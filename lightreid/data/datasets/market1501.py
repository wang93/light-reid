"""
@author:    wangguanan
@contact:   guan.wang0706@gmail.com
"""

import os, copy
from .base import ReIDSamples


class Market1501(ReIDSamples):
    """Market1501.
    Reference:
        Zheng et al. Scalable Person Re-identification: A Benchmark. ICCV 2015.
    URL: `<http://www.liangzheng.org/Project/project_reid.html>`_
    Dataset statistics:
        - identities: 1501 (+1 for background).
        - images: 12936 (train) + 3368 (query) + 15913 (gallery).
    Args:
        data_path(str): path to Market-1501 dataset
        combineall(bool): combine train and test sets as train set if True
    """

    def __init__(self, data_path, combineall=False):
        super(Market1501, self).__init__()

        # parameters
        self.market_path = data_path
        self.combineall = combineall

        # paths of train, query and gallery
        train_path = os.path.join(self.market_path, 'bounding_box_train/')
        query_path = os.path.join(self.market_path, 'query/')
        gallery_path = os.path.join(self.market_path, 'bounding_box_test/')

        # load samples
        train = self._load_samples(train_path)
        query = self._load_samples(query_path)
        gallery = self._load_samples(gallery_path)
        if self.combineall:
            train += copy.deepcopy(query) + copy.deepcopy(gallery)
        train = self.relabel(train)
        self.statistics(train, query, gallery)

        # return
        self.train, self.query, self.gallery = train, query, gallery

    def _load_samples(self, folder_dir):
        '''return (img_path, identity_id, camera_id)'''
        samples = []
        root_path, _, files_name = self.os_walk(folder_dir)
        for file_name in files_name:
            if '.jpg' in file_name:
                person_id, camera_id = self._analysis_file_name(file_name)
                samples.append([root_path+file_name, person_id, camera_id])
        return samples

    def _analysis_file_name(self, file_name):
        '''
        :param file_name: format like 0844_c3s2_107328_01.jpg
        :return: 0844, 3
        '''
        split_list = file_name.replace('.jpg', '').replace('c', '').replace('s', '_').split('_')
        person_id, camera_id = int(split_list[0]), int(split_list[1])
        return person_id, camera_id
