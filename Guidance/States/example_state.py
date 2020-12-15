from Guidance.GuidanceEnums import BehavioralStates


class ExampleState():

    def __init__(self):
        # This function can have whatever params you want.
        pass

    def execute(self, robotData, stateArgs):
        # This is the function that will get executed in a loop.
        # This should be as short as possible
        # the return value is true if the state is done and ready to transition to the next state
        # false if the state is not done
        return False

    def getType(self):
        # Example
        return BehavioralStates.STOP

    def getNextState(self):
        # returns the next state to go to after this one
        # should be a tuple of (behavioral state, stateArgs) or None (None means STOP)
        return (BehavioralStates.STOP, None)
