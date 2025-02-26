
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
    UNDEF = "UNDEF"

class TrafficLightState():
    def __init__(self):
        self.logger = getMainLogger()
        self.id = "TrafficLight"
    
    def updateStatus(self, node : BaseNodeWithState, path : str) -> bool:
        success = True
        reasoning = "UNDEF"
        
        for child in node.childs:
            childPath = str.join("/", [path, child.name])

            # iterate in tree
            if isinstance(child, BaseNodeWithState):
                success = self.updateStatus(child, childPath)
            else:
                self.logger.error("Found node [{}] in tree which is not a status node, abort.".format(
                    childPath
                ))
                reasoning = "Node is not a BaseNodeWithStatus"
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
                reasoning = "All good, done!"
            elif node.state >= NodeState.REVIEWED:
                defaultStatus = TrafficLightStatusColor.YELLOW
                if not planExists:
                    status = defaultStatus
                    reasoning = "Reviewed and no plan date for CLOSED"
                else:
                    status, reasoning = self.calculateStatus(node, childMetaPlan, 'REVIEWED', ['CLOSED'], defaultStatus)
            elif node.state >= NodeState.AVAILABLE:
                defaultStatus = TrafficLightStatusColor.ORANGE
                if not planExists:
                    status = defaultStatus
                else:
                    status, reasoning = self.calculateStatus(node, childMetaPlan, 'AVAILABLE', ['REVIEWED', 'CLOSED'], defaultStatus)
            elif node.state >= NodeState.UNDEF:
                defaultStatus = TrafficLightStatusColor.RED
                if not planExists:
                    status = defaultStatus
                else:
                    status, reasoning = self.calculateStatus(node, childMetaPlan, 'UNDEF', ['AVAILABLE', 'REVIEWED', 'CLOSED'], defaultStatus)

        node.setStatus(self.id, status, reasoning)
        return success

        
    def calculateStatus(
            self,
            node : BaseNodeWithState, 
            childMetaPlan, 
            state : str,
            nextStates : list, 
            defaultStatus : TrafficLightStatusColor) -> tuple[TrafficLightStatusColor, str]:
        
        result = TrafficLightStatusColor.RED
        reasoning = "UNDEF"
        
        # check for this state plan
        now = utcDateTime()
        planExists, planItem = node.getStateDict(childMetaPlan, state)
        if planExists:
            if now <= planItem['targetDate'].when:
                result = TrafficLightStatusColor.GREEN
                reasoning = "Reached [{}] in time (at or before milestone time) [{}]".format(
                    state,
                    planItem['targetDate'].when
                )
            else:
                result = TrafficLightStatusColor.RED  # post milestone default
                reasoning = "Still in [{}] in after milestone time [{}]".format(
                    state,
                    planItem['targetDate'].when
                )

                # no milestone for this state or we passed it, check next states milestones
                for nextState in nextStates:
                    planExists, planItem = node.getStateDict(childMetaPlan, nextState)
                    if planExists:
                        break

                if planExists:
                    # check for next milestone time
                    print((planItem['targetDate'].when - now).total_seconds())
                    diffWeeks = (planItem['targetDate'].when - now).total_seconds() / (60 * 60 * 24 * 7)
                    
                    # TODO: define user defined buffer times
                    if diffWeeks >= 8:
                        result = TrafficLightStatusColor.GREEN
                    elif diffWeeks >= 4:
                        result = TrafficLightStatusColor.YELLOW
                    elif diffWeeks >= 2:
                        result = TrafficLightStatusColor.ORANGE
                    else:
                        result = TrafficLightStatusColor.RED

                    if diffWeeks > 0:
                        reasoning = "Next state [{}] is about [{}] weeks ahead [{}]".format(
                            nextState,
                            int(diffWeeks),
                            planItem['targetDate'].when
                        )                        
                    else:
                        reasoning = "Next state [{}] should have been reached about [{}] weeks ago [{}]".format(
                            nextState,
                            abs(int(diffWeeks)),
                            planItem['targetDate'].when
                        )                        

        return result, reasoning
