import datetime
import winsound
def alarm(Timing):
      alarmtime =str(datetime.datetime.now().strptime(Timing,"%I:%M %p"))
      alarmtime=alarmtime[11:-3]
      realtime=alarmtime[:2]
      realtime=int(realtime)
      Mytime=alarmtime[3:5]
      Mytime=int(Mytime)
      print(f"alarm is set for {Timing}")
      while True:
            if realtime== datetime.datetime.now().hour:
                  if Mytime==datetime.datetime.now().minute:
                        print("it's time")
                        winsound.PlaySound("abc",winsound.SND_LOOP)
            elif Mytime<datetime.datetime.now().minute:
                  break
if __name__=="__main__":
      alarm("12:50 AM")