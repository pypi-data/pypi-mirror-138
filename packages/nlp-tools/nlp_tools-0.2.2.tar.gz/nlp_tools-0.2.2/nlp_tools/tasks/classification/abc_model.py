import os
import json
from abc import ABC
from typing import List,Dict,Any,Union
from sklearn import metrics as sklearn_metrics

import nlp_tools
from nlp_tools.layers import L


from nlp_tools.tasks.abs_task_model import ABCTaskModel
from nlp_tools.types import TextSamplesVar,ClassificationLabelVar,MultiLabelClassificationLabelVar

from nlp_tools.embeddings import ABCEmbedding,TransformerEmbedding,BertEmbedding
from nlp_tools.optimizer import MultiOptimizer
from tensorflow.keras.optimizers import Adam

#from transformers.optimization_tf import AdamWeightDecay
from nlp_tools.loss.r_drop_loss import RDropLoss

from nlp_tools.metrics.plot.confusion_seaborn import plot_confusion_mat

class ABCClassificationModel(ABCTaskModel,ABC):
    """
    Abstract Classification Model
    """

    __task__ = 'classification'

    def to_dict(self) -> Dict:
        info = super(ABCClassificationModel, self).to_dict()
        return info

    def __init__(self,
                 text_processor,
                 label_processor,
                 embedding: ABCEmbedding = None,
                 max_sequence_length: int = None,
                 hyper_parameters: Dict[str, Dict[str, Any]] = None,
                 train_sequece_length_as_max_sequence_length=False,
                 use_FGM=True,
                 use_rdrop=True):

        super(ABCClassificationModel, self).__init__(text_processor=text_processor,label_processor=label_processor,
                                                     embedding=embedding,max_sequence_length=max_sequence_length,hyper_parameters=hyper_parameters,
                                                     train_sequece_length_as_max_sequence_length=train_sequece_length_as_max_sequence_length,
                                                     use_FGM=use_FGM,use_rdrop=use_rdrop)
    def _activation_layer(self) -> L.Layer:
        # if self.multi_label:
        #     return L.Activation('sigmoid')
        # else:
        return L.Activation('softmax')




    def build_model_arc(self) -> None:
        raise NotImplementedError

    def compile_model(self,
                      loss: Any = None,
                      optimizer: Any = None,
                      metrics: Any = None,
                      **kwargs: Any) -> None:

        if loss is None:
            from nlp_tools.loss import multi_category_focal_loss2_fixed
            from tensorflow.keras.losses import SparseCategoricalCrossentropy
            from nlp_tools.loss import categorical_focal_loss
            loss = SparseCategoricalCrossentropy()
            #loss = multi_category_focal_loss2_fixed

        if type(self.embedding) in [TransformerEmbedding, BertEmbedding]:
            total_layers = self.tf_model.layers
            transfomer_layers = self.embedding.embed_model.layers
            no_transformer_layers = [layer for layer in total_layers if layer not in transfomer_layers]
            optimizer_list = [
                Adam(),
                Adam(learning_rate=1e-5)
            ]
            optimizers_and_layers = [(optimizer_list[0], no_transformer_layers), (optimizer_list[1], transfomer_layers)]
            optimizer = MultiOptimizer(optimizers_and_layers)
        else:
            optimizer = Adam(1e-5)
        if self.use_rdrop:
            if type(loss) == list:
                loss = [RDropLoss(i) for i in loss]
            else:
                loss = RDropLoss(loss)

        #optimizer = Adam()#AdamW(weight_decay=0.0)
        if metrics is None:
            metrics = ['accuracy']

        self.tf_model.compile(loss=loss,
                              optimizer=optimizer,
                              metrics=metrics,
                              **kwargs)




    def predict(self,
                x_data: TextSamplesVar,
                *,
                batch_size: int = 32,
                truncating: bool = False,
                multi_label_threshold: float = 0.5,
                predict_kwargs: Dict = None,
                return_labels=True) -> Union[ClassificationLabelVar, MultiLabelClassificationLabelVar]:
        if predict_kwargs is None:
            predict_kwargs = {}

        with nlp_tools.utils.custom_object_scope():
            if truncating:
                seq_length = self.max_sequence_length
            else:
                seq_length = None
            tensor = self.text_processor.transform(x_data,seq_length=seq_length)
            pred = self.tf_model.predict(tensor, batch_size=batch_size, **predict_kwargs)
            pred_argmax = pred.argmax(-1)
            if return_labels:
                res = self.label_processor.inverse_transform(pred_argmax)
            else:
                res = pred_argmax

        return res

    def evaluate(self,
                 valid_data,
                 *,
                 batch_size: int = 32,
                 digits: int = 4,
                 multi_label_threshold: float = 0.5,
                 result_save_path = None):
        x_data = [item[0] for item in valid_data]
        y_data = [item[1] for item in valid_data]
        y_pred_ids = self.predict(x_data,
                              batch_size=batch_size,
                              multi_label_threshold=multi_label_threshold,
                              return_labels=False)

        valid_y_ids = self.label_processor.transform([y for y in y_data])
        label_names = [key for key in self.label_processor.vocab2idx.keys()]

        original_report = sklearn_metrics.classification_report(valid_y_ids,
                                                                y_pred_ids,
                                                                digits=digits,
                                                                target_names=label_names)
        print(original_report)
        if result_save_path:
            if not os.path.exists(result_save_path):
                os.mkdir(result_save_path)
            confusion_save_path = os.path.join(result_save_path, 'confusion.jpg')
            classify_report_path = os.path.join(result_save_path, 'classify_report.txt')
            figure = plot_confusion_mat(valid_y_ids, y_pred_ids, label_names)
            figure.savefig(confusion_save_path, dpi=600)

            with open(classify_report_path,'w',encoding='utf-8') as fwrite:
                if type(original_report) == dict:
                    original_report = json.dumps(original_report,indent=4,ensure_ascii=False)
                fwrite.write(original_report)

