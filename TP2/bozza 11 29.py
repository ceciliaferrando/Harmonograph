# class Pendulum(object):
#     def __init__(self,frequency,amplitude,damping, phase):
#         self.frequency=frequency
#         self.amplitude=amplitude
#         self.damping=damping
#         self.phase=phase
#         
#     def xPen(self, other, t):
#         #"the motion of a rod connected to the bottom of the pendulum along one 
        #axes" from Wikipedia
#         self.amplitude=getAmplitude(self,t)
#         other.amplitude=getAmplitude(other,t)
#         xPen=((self.amplitude*math.sin(self.frequency*t+
                     self.phase)*math.exp(-self.damping*t)+
                (other.amplitude*math.sin(other.frequency*t+
#                      other.phase)*math.exp(-other.damping*t)))