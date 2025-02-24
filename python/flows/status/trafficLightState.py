
from enum import Enum

from python.flows.status.baseNodeWithState import BaseNodeWithState, NodeState
from python.infra.jsonStuff import getFieldSave
from python.infra.logging import getMainLogger
from python.infra.timeStampMeta import utcDateTime


class TrafficLightStatusColor(str, Enum):
    RED = "RED"
    ORANGE = "ORANGE"
    YELLOW = "YELLOW"
    GREEN = "GREEN"

class TrafficLightState():
    def __init__(self):
        self.logger = getMainLogger()
        self.id = "TrafficLight"
    
    def updateStatus(self, node : BaseNodeWithState, path : str) -> bool:
        success = True
        
        for child in node.childs:
            childPath = str.join("/", [path, child.name])

            # iterate in tree
            if isinstance(child, BaseNodeWithState):
                success = self.updateStatus(child, childPath)
            else:
                self.logger.error("Found node [{}] in tree which is not a status node, abort.".format(
                    childPath
                ))
                success = False
                break

        if success:
            # plan is optional for state, only relevant for e.g. traffic light status
            planExists, childMeta = getFieldSave(node.properties, 'meta', None)
            if planExists:
                planExists, childMetaPlan = getFieldSave(childMeta, 'plan', None)

            if not planExists:
                self.logger.error("Unable to identify state plan of [{}] due to missing meta data.".format(
                    path
                ))

            if node.state == NodeState.CLOSED:
                status = TrafficLightStatusColor.GREEN
            elif node.state >= NodeState.REVIEWED:
                defaultStatus = TrafficLightStatusColor.YELLOW
                if not planExists:
                    status = defaultStatus
                else:
                    status = self.calculateStatus(node, childMetaPlan, 'REVIEWED', ['CLOSED'], defaultStatus)
            elif node.state >= NodeState.AVAILABLE:
                defaultStatus = TrafficLightStatusColor.ORANGE
                if not planExists:
                    status = defaultStatus
                else:
                    status = self.calculateStatus(node, childMetaPlan, 'AVAILABLE', ['REVIEWED', 'CLOSED'], defaultStatus)
            elif node.state >= NodeState.UNDEF:
                defaultStatus = TrafficLightStatusColor.RED
                if not planExists:
                    status = defaultStatus
                else:
                    status = self.calculateStatus(node, childMetaPlan, 'UNDEF', ['AVAILABLE', 'REVIEWED', 'CLOSED'], defaultStatus)

        node.setStatus(self.id, status)
        return success

        
    def calculateStatus(
            self,
            node : BaseNodeWithState, 
            childMetaPlan, 
            state : str,
            nextStates : list, 
            defaultStatus : TrafficLightStatusColor) -> TrafficLightStatusColor:
        
        result = TrafficLightStatusColor.RED
        
        # check for this state plan
        now = utcDateTime()
        planExists, planItem = node.getStateDict(childMetaPlan, state)
        if planExists:
            if now <= planItem['targetDate'].when:
                result = TrafficLightStatusColor.GREEN
            else:
                result = TrafficLightStatusColor.RED  # post milestone default

                # no milestone for this state or we passed it, check next states milestones
                for nextState in nextStates:
                    planExists, planItem = node.getStateDict(childMetaPlan, nextState)
                    if planExists:
                        break

                if planExists:
                    # check for next milestone time
                    print((planItem['targetDate'].when - now).total_seconds())
                    diffWeeks = (planItem['targetDate'].when - now).total_seconds() / (60 * 60 * 24 * 7)
                    
                    # TODO: find user defined buffer times
                    if diffWeeks >= 8:
                        result = TrafficLightStatusColor.GREEN
                    elif diffWeeks >= 4:
                        result = TrafficLightStatusColor.YELLOW
                    elif diffWeeks >= 2:
                        result = TrafficLightStatusColor.ORANGE
                    else:
                        result = TrafficLightStatusColor.RED

        return result
