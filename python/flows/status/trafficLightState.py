
from enum import Enum

from python.elements.baseNode import NodeReturnValue
from python.flows.status.baseNodeWithState import BaseNodeWithState, NodeState
from python.infra.logging import getMainLogger


class TrafficLightStatusColor(str, Enum):
    RED = "RED"
    ORANGE = "ORANGE"
    YELLOW = "YELLOW"
    GREEN = "GREEN"

class TrafficLightState():
    def __init__(self):
        self.logger = getMainLogger()
        pass
    


    def statusAsColor(self, status : float) -> tuple[NodeReturnValue, StatusColor]:
        result : StatusColor

        if abs(status) > 1:
            retValue = NodeReturnValue.FAILURE
            self.logger.error("tatus out of boundaries [{}], should be in (-1,1).".format(
                status
            ))
        else:  
            retValue = NodeReturnValue.OK
            if status < 0:
                result = StatusColor.RED
            elif status < 0.5:
                result = StatusColor.ORANGE
            elif status < 1:
                result = StatusColor.YELLOW
            else:
                result = StatusColor.GREEN

        return retValue, result

    # status calculation
    # check meta.goal and meta.status to identify how ready we are 
    def updateStateWithMetaData(self, path : str) -> tuple[bool, float]:
        success = True
        result = NodeState(NodeState.UNDEF)

        fieldExists, childMeta = getFieldSave(self.properties, 'meta', None)
        if fieldExists:
            fieldExists, childMetaPlan = getFieldSave(self.properties['meta'], 'plan', None)

        if not fieldExists:
            self.logger.error("Unable to identify status of [{}] due to missing meta data.".format(
                path
            )) 
            success = False
        else:
            # we got the plan for the child, compare to reality
            fieldExists, childMetaStatus = getFieldSave(self.properties['meta'], 'state', None)
            
            if not fieldExists:
                newChildStatus = NodeState(NodeState.UNDEF)
            else:

                # calculate time until REQUIRED data, if shorter than X -> 
                '''
                class NodeStatus(float, Enum):
                    UNDEF = -1
                    AVAILABLE = 0
                    REVIEWED = 0.5
                    CLOSED = 1
                '''
                # TODO: if status.has(CLOSED) -> CLOSED
                #       elif status.has(REVIEWED) -> REVIEWED
                #       elif status.has(AVAILALBLE) -> AVAILABLE
                #       else
                #           status -> UNDEF
                #           if goal.has(AVAILABLE): // need time to review
                #             if time(AVAILABLE) in past or present + 1 WK -> -0.1
                #             elif time(AVAILABLE) + 1 M -> color = 0.4 TODO create function with input color, output largest possible float
                #             elif time(AVAILABLE) + 3 M -> color = StatusColor.YELLOW (0.9)
                #             else color = StatusColor.GREEN (1)
                #           if goal.has(REVIEWED):
                #             if time(REVIEWED) in past or present + 1 M -> color = StatusColor.RED
                #             elif time(REVIEWED) + 3 M -> color = StatusColor.ORANGE
                #             elif time(REVIEWED) + 6  M -> color = StatusColor.YELLOW
                #             else color = StatusColor.GREEN
                #           if goal.has(CLOSED):
                #             if time(CLOSED) in past or present + 1 M -> color = StatusColor.RED
                #             elif time(CLOSED) + 3 M -> color = StatusColor.ORANGE
                #             elif time(CLOSED) + 6  M -> color = StatusColor.YELLOW
                #             else color = StatusColor.GREEN

            rollUpStatus, newChildStatus, statusColor = self.rolledUpState()
            if rollUpStatus != NodeReturnValue.OK:
                newChildStatus = NodeState.UNDEF
                self.logger.error("Failure during status roll up, set status of node [{}] to [{}].".format(
                    path,
                    newChildStatus
                ))
            else:
                self.logger.debug("Set status of [{}] to {}[{}].".format(
                    path,
                    statusColor,
                    newChildStatus
                ))
                

        self.state = newChildStatus


        return success, result