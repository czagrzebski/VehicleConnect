import json

obd_json = json.dumps([
    {'type': 'title',
      'title': 'OBD Settings'},

      {'type': 'string',
      'title': 'OBD Port',
      'desc': 'Set default OBD port',
      'section': 'OBD',
      'key': 'obdport'},
      
      {'type': 'string',
      'title': 'OBD Mac Address',
      'desc': 'Adapter Mac Address',
      'section': 'OBD',
      'key': 'obdmacaddress'},
    
      
      
      ])

vehicle_json = json.dumps([

      
      {'type': 'title',
      'title': 'Gear Setup'},
      
      {'type': 'string',
      'title': 'First Gear',
      'desc': 'Transmission Ratio',
      'section': 'Vehicle',
      'key': 'firstGear'},


      {'type': 'string',
      'title': 'Second Gear',
      'desc': 'Transmission Ratio',
      'section': 'Vehicle',
      'key': 'secondGear'},


      {'type': 'string',
      'title': 'Third Gear',
      'desc': 'Transmission Ratio',
      'section': 'Vehicle',
      'key': 'thirdGear'},

      {'type': 'string',
      'title': 'Fourth Gear',
      'desc': 'Transmission Ratio',
      'section': 'Vehicle',
      'key': 'fourthGear'},


      {'type': 'string',
      'title': 'Fifth Gear',
      'desc': 'Transmission Ratio',
      'section': 'Vehicle',
      'key': 'fifthGear'},


       {'type': 'string',
      'title': 'Sixth Gear',
      'desc': 'Transmission Ratio',
      'section': 'Vehicle',
      'key': 'sixthGear'},

       
      {'type': 'title',
      'title': 'Axle Setup'},
      
      {'type': 'string',
      'title': 'Axle Ratio',
      'desc': 'Rear Axle Ratio',
      'section': 'Vehicle',
      'key': 'axelRatio'},

      {'type': 'title',
      'title': 'Tire'},
      
      {'type': 'string',
      'title': 'Tire Diamater',
      'desc': 'Tire Diamater (Inches)',
      'section': 'Vehicle',
      'key': 'tireDiamater'},

      {'type': 'title',
      'title': 'Performance'},

      {'type': 'string',
      'title': 'Max RPM',
      'desc': 'Maximimum RPM',
      'section': 'Vehicle',
      'key': 'maxRPM'}

      
      ])
      
     