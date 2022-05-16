
 var data_for_map;
 $(document).ready( function () {
 
  $.ajax({
    url: '/get_map_data',         
    method: 'get', 
    async: false,             
    dataType: 'json',          
      
    success: function(data){       
      data_for_map= data; 
      console.log('success ajax')  
    }
  });
  console.log('1')
  console.log(data_for_map.data)
  massLine = []
  massBabble = []
  for (var i = 0; i < data_for_map.data.length; i++) {

       


      objLine= {
        origin: {
            latitude: parseFloat(data_for_map.data[i].long1),
            longitude:parseFloat(data_for_map.data[i].lat1)
        },
        destination: {
            latitude: parseFloat(data_for_map.data[i].long2),
            longitude:parseFloat( data_for_map.data[i].lat2)
        }
      }

      objBabble1=
        {
          name: data_for_map.data[i].source_ip +" "+ data_for_map.data[i].country1 + " "+ data_for_map.data[i].city1, 
          latitude:  parseFloat(data_for_map.data[i].long1),
          longitude: parseFloat(data_for_map.data[i].lat1),
          radius: 5, 
          fillKey: 'gt50'
        }
    
      objBabble2=
        {
          name: data_for_map.data[i].destination +" " +data_for_map.data[i].country2 +" " + data_for_map.data[i].city2 , 
          latitude:  parseFloat(data_for_map.data[i].long2),
          longitude: parseFloat(data_for_map.data[i].lat2),
          radius:5, 
          fillKey: 'gt10'
        }


        massBabble.push(objBabble1)
        massBabble.push(objBabble2)
        massLine.push(objLine)
     
  }

  console.log(massBabble)
   

  var map = new Datamap({
    scope: 'world',
    element: document.getElementById('map'),
    projection: 'mercator',

    fills: {
      defaultFill: '#00000a',    
    },
  })


  map.arc(massLine, {strokeWidth: 1});

    
  map.bubbles(massBabble, {
    popupTemplate: function(geo, data) {
      return "<div class='hoverinfo'>It is " + data.name + "</div>";
    }
  });

  

 })

//   $('#table_id').DataTable( {
//     data: data_for_map.data,
//     columns: [
//         { data: 'source_ip' },
//         { data: 'destination_ip' },
//         { data: 'id_pack' },
//     ]
// } );

 

// massLine = []
// massBabble = []
// for (var i = 0; i < data_for_map.data.length; i++) {
 
//   // if( data_for_map.data[i].lat1 !=  data_for_map.data[i].lat2){
//   //   if( data_for_map.data[i].long1 !=  data_for_map.data[i].long2){

//   //     objLine= {
//   //       origin: {
//   //           latitude: parseFloat(data_for_map.data[i].lat1),
//   //           longitude:parseFloat(data_for_map.data[i].long1)
//   //       },
//   //       destination: {
//   //           latitude: parseFloat(data_for_map.data[i].lat2),
//   //           longitude:parseFloat( data_for_map.data[i].long2)
//   //       }
//   //     }
    
//       objBabble1=
//         {
//           name: data_for_map.data[i].city1, 
//           latitude:  parseFloat(data_for_map.data[i].lat1),
//           longitude: parseFloat(data_for_map.data[i].long1),
//           radius: 5, 
//           fillKey: 'gt50'
//         }
    
//         objBabble2=
//         {
//           name: data_for_map.data[i].city2, 
//           latitude:  parseFloat(data_for_map.data[i].lat2),
//           longitude: parseFloat(data_for_map.data[i].long2),
//           radius:5, 
//           fillKey: 'gt50'
//         }
  
  
//     if (!massBabble.includes(objBabble1)){
//       massBabble.push(objBabble1)
//     }
//     if (!massBabble.includes(objBabble2)){
//       massBabble.push(objBabble2)
//     }
//     // if (!massLine.includes(objLine)){
//     //   massLine.push(objLine)

//     // }
     
// }




 


// console.log(massLine.length)
// console.log(massBabble.length)

// map.arc(massLine, {strokeWidth: 1});

  
// map.bubbles(massBabble, {
//   popupTemplate: function(geo, data) {
//     return "<div class='hoverinfo'>It is " + data.name + "</div>";
//   }
// });


// } );



