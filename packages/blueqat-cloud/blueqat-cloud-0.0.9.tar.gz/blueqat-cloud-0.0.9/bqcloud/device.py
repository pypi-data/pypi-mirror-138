from enum import Enum


class Device(str, Enum):
    Local = "local"
    IonQDevice = "aws/ionq/ionQdevice"
    Aspen11 = "aws/rigetti/Aspen-11"
    AspenM1 = "aws/rigetti/Aspen-M-1"
    SimSv1 = "aws/amazon/sv1"
    SimTn1 = "aws/amazon/tn1"
    SimDm1 = "aws/amazon/dm1"
