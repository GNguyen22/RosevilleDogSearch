var express = require('express');
var router = express.Router();

let {PythonShell} = require('python-shell')

//database variables
var sqlite3 = require('sqlite3').verbose();
var db = new sqlite3.Database('DogsForAdoption.db')


router.get('/', function(req, res, next) {
   getDoggoData(res);
});

module.exports = router;

function getDoggoData(res) {
   //db.serialize(function () {
      db.all("SELECT * FROM DogInfo", function(err, allRows) {
         //console.log(allRows)
         if(err != null) {
            console.log(err);
            callback(err);
         }
         res.json(
            allRows
         );
      });
   //});
}

function scrapeDoggoData() {
   //res.send('respond with a resource');
   let options = {
      pythonPath: 'python2'
   }
   PythonShell.run('placerDogs.py', options, function (err, results) {
      if (err) throw err;
      console.log('results: %j', results);
      storeDoggoData(JSON.parse(results));
      console.log('done');
   });
}

module.exports.scrapeDoggoData = scrapeDoggoData;


function storeDoggoData(results) {

   //database code
   db.serialize(function () {
      db.run('DROP TABLE if exists DogInfo');
      db.run('CREATE TABLE DogInfo (doggo TEXT, name TEXT, sexSN TEXT, breed TEXT, age TEXT, intake TEXT, id TEXT, species TEXT, dogLink TEXT)');
      //var stmt = db.prepare('INSERT INTO DogInfo (img, name, sexSN, breed, age, intake) VALUES (?, ?, ?, ?, ?, ?)');

      for (var i = 0; i < results.length; i++) {
         values = results[i]
         const cols = Object.keys(values).join(", ");
         const placeholders = Object.keys(values).fill('?').join(", ");
         db.run('INSERT INTO DogInfo (' + cols + ')' +
                ' VALUES ' +
                '(' + placeholders + ')',
            Object.values(values),
            (err) => {
               if (err) {
                  console.log(err)
               }
               //console.log("Stored things");
            });
      }
   })

   //db.close()
}
