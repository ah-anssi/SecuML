# SecuML
# Copyright (C) 2018  ANSSI
#
# SecuML is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# SecuML is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with SecuML. If not, see <http://www.gnu.org/licenses/>.

import inspect

from SecuML.core.Classification.Configuration.AlertsConfiguration \
        import AlertsConfiguration
from SecuML.core.Clustering.Configuration import ClusteringConfFactory

test_conf_factory = None


def getFactory():
    global test_conf_factory
    if test_conf_factory is None:
        test_conf_factory = TestConfFactory()
    return test_conf_factory

def generateAlertConfFromArgs(args):
    params = {}
    params['num_clusters'] = args.num_clusters
    params['num_results'] = None
    params['projection_conf'] = None
    params['label'] = 'all'
    clustering_conf = ClusteringConfFactory.getFactory().fromParam(
        args.clustering_algo,
        params)
    alerts_conf = AlertsConfiguration(args.top_n_alerts,
                                      args.detection_threshold,
                                      clustering_conf)
    return alerts_conf

class TestConfFactory(object):

    def __init__(self):
        self.register = {}

    def registerClass(self, class_name, class_obj):
        self.register[class_name] = class_obj

    def fromJson(self, obj):
        class_name = obj['__type__']
        obj = self.register[class_name].fromJson(obj)
        return obj

    def fromParam(self, test_method, args, logger=None):
        class_ = self.register[test_method + 'Conf']
        param = list(inspect.signature(class_.__init__).parameters.keys())
        param.remove('self')
        args['logger'] = logger
        args = [args[key] if key in args else None for key in param]
        obj = class_(*args)
        return obj

    def fromArgs(self, test_method, args, logger=None):
        class_ = self.register[test_method + 'Conf']
        params = class_.generateParamsFromArgs(args)
        return self.fromParam(test_method, params, logger=logger)
