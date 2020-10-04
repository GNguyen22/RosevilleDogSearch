var createError = require('http-errors');
var express = require('express');
var path = require('path');
var cookieParser = require('cookie-parser');
var logger = require('morgan');

var app = express();

var indexRouter = require('./routes/index');
var usersRouter = require('./routes/users');
var doggoDataRouter = require('./routes/doggo-data');


// view engine setup
app.set('views', path.join(__dirname, 'views'));
app.set('view engine', 'jade');

app.use(logger('dev'));
app.use(express.json());
app.use(express.urlencoded({ extended: false }));
app.use(cookieParser());
app.use(express.static(path.join(__dirname, 'public')));

app.use('/', indexRouter);
app.use('/users', usersRouter);
app.use('/retrieve-doggo-data', doggoDataRouter);

// ssl certificate


app.enable('trust proxy');
app.use (function (req, res, next) {
	//console.log("beginning: matt is the pretttttttttttttttiest");
        if (req.secure) {
                // request was via https, so do no special handling
                //console.log("if: matt is prettiest");
                next();
        } else {
                // request was via http, so redirect to https
		//console.log("else: matt is pretty");
                return res.redirect('https://' + req.headers.host + req.url);
        }
});

// catch 404 and forward to error handler
app.use(function(req, res, next) {
  console.log("more errors");
  next(createError(404));
});

// error handler
app.use(function(err, req, res, next) {
  // set locals, only providing error in development
  console.log("error page");
  res.locals.message = err.message;
  res.locals.error = req.app.get('env') === 'development' ? err : {};

  // render the error page
  res.status(err.status || 500);
  res.render('error');
});


module.exports = app;

function callEveryHour() {
   //console.log("in loop");
   setInterval((doggoDataRouter.scrapeDoggoData), 1000*60*60);
}

//doggoDataRouter.scrapeDoggoData();
callEveryHour();
