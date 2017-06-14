# ----------------------------------------------------------------------
# Numenta Platform for Intelligent Computing (NuPIC)
# Copyright (C) 2017, Numenta, Inc.  Unless you have an agreement
# with Numenta, Inc., for a separate license for this software code, the
# following terms and conditions apply:
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero Public License version 3 as
# published by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU Affero Public License for more details.
#
# You should have received a copy of the GNU Affero Public License
# along with this program.  If not, see http://www.gnu.org/licenses.
#
# http://numenta.org/licenses/
# ----------------------------------------------------------------------

"""
This module tests capnp serialization of HTMPredictionModel.
"""

import copy
import datetime
import numpy.random
import unittest

try:
  # NOTE need to import capnp first to activate the magic necessary for
  # PythonDummyRegion_capnp, etc.
  import capnp
except ImportError:
  capnp = None
else:
  from nupic.frameworks.opf.HTMPredictionModelProto_capnp \
    import HTMPredictionModelProto

from nupic.frameworks.opf.model_factory import ModelFactory

from nupic.frameworks.opf.htm_prediction_model import HTMPredictionModel



# Model parameters derived from the Hotgym anomaly example. This example was
# used because it uses the most components.  Some of the parameters, such
# as columnCount were reduced to make the test run faster.


CPP_MODEL_PARAMS = {
    'model': 'HTMPrediction',
    'version': 1,
    'aggregationInfo': {  'days': 0,
        'fields': [(u'c1', 'sum'), (u'c0', 'first')],
        'hours': 1,
        'microseconds': 0,
        'milliseconds': 0,
        'minutes': 0,
        'months': 0,
        'seconds': 0,
        'weeks': 0,
        'years': 0},
    'predictAheadTime': None,
    'modelParams': {
      # inferenceType choices:
      #
      # TemporalNextStep, TemporalClassification, NontemporalClassification,
      # TemporalAnomaly, NontemporalAnomaly, TemporalMultiStep,
      # NontemporalMultiStep
      #
      #'inferenceType': 'TemporalAnomaly', # TODO: blocked on NUP-2356
      'inferenceType': 'NontemporalMultiStep',
        'sensorParams': {
            'verbosity' : 0,
            'encoders': {
                u'consumption':    {  'clipInput': True,
                    'fieldname': u'consumption',
                    'maxval': 100.0,
                    'minval': 0.0,
                    'n': 50,
                    'name': u'c1',
                    'type': 'ScalarEncoder',
                    'w': 21},},
            'sensorAutoReset' : None,
        },
        'spEnable': True,
        'spParams': {
            'spatialImp' : 'cpp',
            'spVerbosity' : 0,
            'globalInhibition': 1,
            'columnCount': 512,
            'inputWidth': 0,
            'numActiveColumnsPerInhArea': 20,
            'seed': 1956,
            'potentialPct': 0.5,
            'synPermConnected': 0.1,
            'synPermActiveInc': 0.1,
            'synPermInactiveDec': 0.005,
        },
        'tmEnable' : True,
        'tmParams': {
            'temporalImp': 'cpp',
            'verbosity': 0,
            'columnCount': 512,
            'cellsPerColumn': 8,
            'inputWidth': 512,
            'seed': 1960,
            'newSynapseCount': 10,
            'maxSynapsesPerSegment': 20,
            'maxSegmentsPerCell': 32,
            'initialPerm': 0.21,
            'permanenceInc': 0.1,
            'permanenceDec' : 0.1,
            'globalDecay': 0.0,
            'maxAge': 0,
            'minThreshold': 4,
            'activationThreshold': 6,
            'outputType': 'normal',
            'pamLength': 1,
        },
        'clParams': {
            'implementation': 'cpp',
            'regionName': 'SDRClassifierRegion',
            'verbosity' : 0,
            'alpha': 0.005,
            'steps': '1,5',
        },

        'anomalyParams': {  u'anomalyCacheRecords': None,
    u'autoDetectThreshold': None,
    u'autoDetectWaitRecords': 2184},

        'trainSPNetOnlyIfRequested': False,
    },
}



PY_MODEL_PARAMS = {
  'model': 'HTMPrediction',
    'version': 1,
    'aggregationInfo': {  'days': 0,
                          'fields': [(u'c1', 'sum'), (u'c0', 'first')],
        'hours': 1,
        'microseconds': 0,
        'milliseconds': 0,
        'minutes': 0,
        'months': 0,
        'seconds': 0,
        'weeks': 0,
        'years': 0},
    'predictAheadTime': None,
    'modelParams': {
      # inferenceType choices:
      #
      # TemporalNextStep, TemporalClassification, NontemporalClassification,
      # TemporalAnomaly, NontemporalAnomaly, TemporalMultiStep,
      # NontemporalMultiStep
      #
      #'inferenceType': 'TemporalAnomaly', # TODO: blocked on NUP-2356
      'inferenceType': 'NontemporalMultiStep',
        'sensorParams': {
          'verbosity' : 0,
            'encoders': {
              u'consumption':    {  'clipInput': True,
                                      'fieldname': u'consumption',
                    'maxval': 100.0,
                    'minval': 0.0,
                    'n': 50,
                    'name': u'c1',
                    'type': 'ScalarEncoder',
                    'w': 21},},
            'sensorAutoReset' : None,
            },
        'spEnable': True,
        'spParams': {
          'spatialImp' : 'py',
            'spVerbosity' : 0,
            'globalInhibition': 1,
            'columnCount': 512,
            'inputWidth': 0,
            'numActiveColumnsPerInhArea': 20,
            'seed': 1956,
            'potentialPct': 0.5,
            'synPermConnected': 0.1,
            'synPermActiveInc': 0.1,
            'synPermInactiveDec': 0.005,
            },
        'tmEnable' : True,
        'tmParams': {
          'temporalImp': 'py',
            'verbosity': 0,
            'columnCount': 512,
            'cellsPerColumn': 8,
            'inputWidth': 512,
            'seed': 1960,
            'newSynapseCount': 10,
            'maxSynapsesPerSegment': 20,
            'maxSegmentsPerCell': 32,
            'initialPerm': 0.21,
            'permanenceInc': 0.1,
            'permanenceDec' : 0.1,
            'globalDecay': 0.0,
            'maxAge': 0,
            'minThreshold': 4,
            'activationThreshold': 6,
            'outputType': 'normal',
            'pamLength': 1,
            },
        'clParams': {
          'implementation': 'py',
            'regionName': 'SDRClassifierRegion',
            'verbosity' : 0,
            'alpha': 0.005,
            'steps': '1,5',
            },

        'anomalyParams': {  u'anomalyCacheRecords': None,
                            u'autoDetectThreshold': None,
    u'autoDetectWaitRecords': 2184},

        'trainSPNetOnlyIfRequested': False,
        },
}


class HTMPredictionModelSerializationTest(unittest.TestCase):


  def _runSimpleModelSerializationDeserialization(self, modelParams):
    # Rudimentary serialization/deserialization; flush out starting point for
    # tests

    m1 = ModelFactory.create(modelParams)
    m1.enableInference({'predictedField': 'consumption'})
    headers = ['timestamp', 'consumption']

    record = [datetime.datetime(2013, 12, 12), numpy.random.uniform(100)]
    modelInput = dict(zip(headers, record))
    m1.run(modelInput)

    # Serialize
    builderProto = HTMPredictionModelProto.new_message()
    m1.write(builderProto)

    # Construct HTMPredictionModelProto reader from populated builder
    readerProto = HTMPredictionModelProto.from_bytes(builderProto.to_bytes())

    # Deserialize
    m2 = HTMPredictionModel.read(readerProto)
    # Work around a serialization bug that doesn't save the enabled predicted
    # field
    # TODO this enableInference call should be removed after NUP-2463 is fixed.
    m2.enableInference({'predictedField': 'consumption'})

    # Run computes on m1 & m2 and compare results
    record = [datetime.datetime(2013, 12, 14), numpy.random.uniform(100)]
    modelInput = dict(zip(headers, record))
    # NOTE: use deepcopy to guarantee no side-effect
    r1 = m1.run(copy.deepcopy(modelInput))
    r2 = m2.run(copy.deepcopy(modelInput))

    #self.assertEqual(r1, r2)


  @unittest.skip('NUP-2463 Predicted field and __inferenceEnabled are not '
                 'serialized by HTMPredictionModel.write')
  @unittest.skipUnless(
    capnp, 'pycapnp is not installed, skipping serialization test.')
  def testPredictedFieldAndInferenceEnabledAreSaved(self):
    m1 = ModelFactory.create(PY_MODEL_PARAMS)
    m1.enableInference({'predictedField': 'consumption'})
    self.assertTrue(m1.isInferenceEnabled())
    self.assertEqual(m1.getInferenceArgs().get('predictedField'), 'consumption')


    headers = ['timestamp', 'consumption']

    record = [datetime.datetime(2013, 12, 12), numpy.random.uniform(100)]
    modelInput = dict(zip(headers, record))
    m1.run(modelInput)

    # Serialize
    builderProto = HTMPredictionModelProto.new_message()
    m1.write(builderProto)

    # Construct HTMPredictionModelProto reader from populated builder
    readerProto = HTMPredictionModelProto.from_bytes(builderProto.to_bytes())

    # Deserialize
    m2 = HTMPredictionModel.read(readerProto)

    self.assertTrue(m2.isInferenceEnabled())
    self.assertEqual(m2.getInferenceArgs().get('predictedField'), 'consumption')

    # Running the desrialized m2 without redundant enableInference call should
    # work
    record = [datetime.datetime(2013, 12, 14), numpy.random.uniform(100)]
    modelInput = dict(zip(headers, record))
    m2.run(modelInput)

    # Check that disabled inference is saved, too (since constructor defaults to
    # enabled at time of this writing)
    m1.disableInference()
    self.assertFalse(m1.isInferenceEnabled())
    builderProto = HTMPredictionModelProto.new_message()
    m1.write(builderProto)
    readerProto = HTMPredictionModelProto.from_bytes(builderProto.to_bytes())
    m3 = HTMPredictionModel.read(readerProto)
    self.assertFalse(m3.isInferenceEnabled())



  @unittest.skipUnless(
    capnp, 'pycapnp is not installed, skipping serialization test.')
  def testSimpleCPPModelSerializationNoValidation(self):
    # Rudimentary serialization/deserialization; flush out starting point for
    # tests

    self._runSimpleModelSerializationDeserialization(CPP_MODEL_PARAMS)


  @unittest.skipUnless(
    capnp, 'pycapnp is not installed, skipping serialization test.')
  def testSimplePYModelSerializationNoValidation(self):
    # Rudimentary serialization/deserialization; flush out starting point for
    # tests

    self._runSimpleModelSerializationDeserialization(PY_MODEL_PARAMS)



if __name__ == "__main__":
  unittest.main()
