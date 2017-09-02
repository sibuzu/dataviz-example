var API_URL = 'http://localhost:5000/api'

var displayJSON = function (query) {

  d3.json(API_URL + query, function (error, data) {

    if (error) {
      console.log(error)
    }

    d3.select('#query pre').html(query)
    d3.select('#data pre').html(JSON.stringify(data, null, 4))
    console.log(data)
  })
}

var query = '/winners?where=' + JSON.stringify({
  'year': {'$gt': 2002},
  'gender': 'male'
})

query = '/winners?projection=' + JSON.stringify({
  'mini_bio': 0
})
 
query = '/winners?where=' + JSON.stringify({
  'name': "Albert Einstein"
})

var albertId = '59aaa3dcb6435f0596864350'
query = '/winners/' + albertId

console.log('query: ' + query)
displayJSON(query)
