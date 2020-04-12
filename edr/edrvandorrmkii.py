import edtime

class EDRVanDorrMKII(object):
    PROSPECTOR_SPEED = 200 * 60 * 60 / 1000
    COLLECTOR_SPEED = 200 * 60 * 60 / 1000
    # Ranges are from 1A (1.2km) up to 7A (2.04km), 7B (2.38km ?) https://elite-dangerous.fandom.com/wiki/Limpet_Controller/Collector
    PROSPECTOR_MAX_RANGE = 11.9
    COLLECTOR_MAX_RANGE = 2.38
    LTD_GOOD_PRICE_RANGE = [1.0, 1.7]

    def __init__(self):
        self.prospector_launched_edtime = None
        self.prospector_max_distance = EDRVanDorrMKII.PROSPECTOR_MAX_RANGE
        self.start_time = edtime.EDTime.py_epoch_now()

    def start_stopwatch(self):
        self.start_time = edtime.EDTime.py_epoch_now()

    def assess_asteroid(self, prospected):
        # { "timestamp":"2020-04-03T21:23:10Z", "event":"ProspectedAsteroid",
        # "Materials":[ 
        #  { "Name":"LowTemperatureDiamond", "Name_Localised":"Low Temperature Diamonds", "Proportion":20.509537 }, 
        #  { "Name":"water", "Proportion":1.938108 },
        #  { "Name":"liquidoxygen", "Name_Localised":"Liquid oxygen", "Proportion":2.722850 } ],
        #  "Content":"$AsteroidMaterialContent_Low;", "Content_Localised":"Material Content: Low",
        #  "Remaining":100.000000 }
        header = ""
        details = []
        distance = None
        if self.prospector_launched_edtime:
            reached_time = edtime.EDTime().from_journal_timestamp(prospected["timestamp"])
            time_of_flight = reached_time.as_py_epoch() - self.prospector_launched_edtime.as_py_epoch()
            distance = (time_of_flight / 3600) * EDRVanDorrMKII.PROSPECTOR_SPEED
            if distance > self.prospector_max_distance:
                distance = None
        self.prospector_launched_time = None
        return distance

    def profits_per_hour(self, cargo):
        elapsed_time = edtime.EDTime.py_epoch_now() - self.start_time
        # assess cargo
        profits = 0
        pph = profits / (elapsed_time / (60*60))
        return pph