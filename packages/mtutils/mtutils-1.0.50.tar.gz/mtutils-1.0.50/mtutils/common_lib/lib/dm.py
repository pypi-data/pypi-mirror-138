from email.policy import default
from .data_manager import DataManager as DataManagerBase

from .utils import decode_distribution, encode_distribution
from .anno import AMDet
from .anno import AMML
from .anno import AMMC

import numpy as np
import copy

class DMBase(DataManagerBase):
    def __init__(self, record_list, class_dict):
        assert isinstance(record_list, (list, tuple))
        self.record_list = record_list
        self.class_dict = class_dict


class DMMC(DMBase):
    def __init__(self, *args, **kwargs):
        super(DMMC, self).__init__(*args, **kwargs)
        self.am = AMMC(self.class_dict)
        self.set_class = self.am.set_class
        self.get_classid = self.am.get_classid
        self.get_classname = self.am.get_classname
        self.get_score = self.am.get_score
        self.create_distribution = self.am.create_distribution

    def data_statistics(self):
        class_occurrence = self.occurrence(self.get_classname)
        return {
            'image_number': len(self),
            'class_occurrence': class_occurrence
        }


class DMML(DMBase):
    def __init__(self, *args, **kwargs):
        super(DMML, self).__init__(*args, **kwargs)
        self.am = AMML(self.class_dict)
        self.set_class = self.am.set_class
        self.get_classid = self.am.get_classid
        self.get_classname = self.am.get_classname
        self.get_score = self.am.get_score
        self.create_scores = self.am.create_scores


    def to_mc(self):
        # add OK class to class dict
        class_dict_aug = self.am._add_ok_class(self.class_dict)
        
        # transform record list
        am = self.am.clone()
        am.set_class('leaf')
        record_list = list()
        for rec in self.record_list:
            new_rec = copy.deepcopy(rec['info'])
            new_rec.pop('scores')
            scores_leaf = am.get_score(rec)
            leaf_max_id = np.argmax(scores_leaf)
            ng_score = scores_leaf[leaf_max_id]
            leaf_class_with_max_score = am._label2class[leaf_max_id]
            all_max_id = am._class2label_all[leaf_class_with_max_score]
            distribution_tail = [0]*len(am._class2label_all)
            distribution_tail[all_max_id] = ng_score
            distribution = [1.-ng_score] + distribution_tail
            new_rec['distribution'] = encode_distribution(distribution)
            record_list.append(
                {
                    'info': new_rec
                }
            )

        return DMMC(record_list = record_list, class_dict = class_dict_aug)


    def data_statistics(self):
        return {'image_number': len(self)}


class DMDet(DMBase):
    def __init__(self, *args, **kwargs):
        super(DMDet, self).__init__(*args, **kwargs)
        self.am = AMDet(self.class_dict)
        self.set_class = self.am.set_class
        self.get_classid = self.am.get_classid
        self.get_classname = self.am.get_classname
        self.get_score = self.am.get_score
        self.get_shape = self.am.get_shape
        self.create_instance = self.am.create_instance


    def to_ml(self):
        # transform record list
        num_classes = len(self.class_dict)
        record_list = list()
        for rec in self.record_list:
            new_rec = copy.deepcopy(rec['info'])
            distributions = [[0]*num_classes]
            for inst in rec['instances']:
                if 'class_id' in inst:
                    assert 'score' in inst
                    dist_all = [0]*num_classes
                    dist_all[inst['class_id']] = inst['score']
                else:
                    dist_all = decode_distribution(inst['distribution'])
                distributions.append(dist_all)
            scores = np.max(distributions, axis=0)
            new_rec['scores'] = encode_distribution(scores)
            record_list.append(
                {
                    'info': new_rec
                }
            )

        return DMML(record_list = record_list, class_dict = self.class_dict)

    def to_mc(self):
        data_ml = self.to_ml()
        return data_ml.to_mc()


    def data_statistics(self):
        am = self.am.clone()
        am.set_class('leaf')

        class_occurence_by_instance = self.occurrence(am.get_classname)
        class_occurence_by_image = self.occurrence(lambda rec: list(set(am.get_classname(rec))))
        ok_ng_counter = self.occurrence(lambda rec: len(rec['instances'])>0)

        return {
            'total_images': len(self),
            'ok_images': ok_ng_counter.get(False, 0),
            'ng_images': ok_ng_counter.get(True,  0),
            'class_occurence_by_image': class_occurence_by_image,
            'class_occurence_by_instance': class_occurence_by_instance
        }