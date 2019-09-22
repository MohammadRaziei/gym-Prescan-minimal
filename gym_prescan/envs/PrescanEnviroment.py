from gym_prescan.envs.PrescanModel import *




class Enviroment:
    def __init__(self,outport=None, inport=None):
        self.outport = outport
        self.out = Reciver_UDP_json(outport)
        self.out.build()

        self.inport = inport
        self.inp = Transmitter_UDP(inport,fmt='ddd')


    def __del__(self):
        self.close()

    def close(self):
        self.out.close()
        self.inp.close()
        # self.off_set_UDP.close()
        # self.desired_velocity_UDP.close()
        # self.reset_UDP.close()
        for model in Model.objects:
            model.close()
        try:
            eng.quit()
        except:
            pass
        # print('Enviroment-------close')

    def reset(self):
        # self.reset_UDP.send(True)
        # self.reset_UDP.send(False)
        # self.send((0,0))
        self.send_vec([0,0,1])

        while True:
            self.get()
            if not self.done:
                break
        self.send_vec([0,0,0])
        return 

    def send_vec(self,data):
        o = data[0];v = data[1];r = data[2]
        self.inp.send(o,v,r)

    def send(self,data):
        o = data[0];v = data[1]
        self.inp.send(o,v,0)
        # self.off_set_UDP.send(o)
        # self.desired_velocity_UDP.send(v)
        # self.reset_UDP.send(r,'?')

    def get(self):
        self.data = self.out.get()
        self.agent = self.data['Vehicles'][self.data['Object']]
        self.collision = self.data['Collision']
        # self.collision['Occurred'] = bool(self.collision['Occurred'])
        self.done = bool(self.data['done'])
        return self.data

    def create_model(self, car_name=None, road_name=None):
        self.road = Road(road_name)
        self.car = Vehicle(car_name, self.road)
        self.road.create()
        self.car.create()

        # print('_____________env______________')

