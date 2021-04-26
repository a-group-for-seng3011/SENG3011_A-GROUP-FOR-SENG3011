const express = require('express');

const router = express.Router();

const ONE_HOUR_IN_MILLISECONDS = 60 * 60 * 1000;

const getUserDateInTimezone = offsetInHours => {
  const utcDate = Date.now();
  
  const offsetInMilliseconds = ONE_HOUR_IN_MILLISECONDS * offsetInHours;
  
  return new Date(utcDate + offsetInMilliseconds);
};

router.get('/', (request, response) => {
  const {timezone = 0} = request.query;
  
  const userDateInTimezone = getUserDateInTimezone(timezone);
  
  var date = new Date();
  var pastMonth = date.getMonth() - 6;
  if (pastMonth <= 0) {
    pastMonth += 12;
    date.setFullYear(date.getFullYear() - 1);
  }
  date.setMonth(pastMonth);
  console.log(date);
  var isoTime1 = date.toISOString();
  var arr1 = isoTime1.split('.');
  var start_time = arr1[0];
  
  var isoTime2 = userDateInTimezone.toISOString();
  var arr2 = isoTime2.split('.');
  var end_time = arr2[0];
  const dateObject = {
    day: userDateInTimezone.getDate(),
    month: userDateInTimezone.getMonth() + 1,
    year: userDateInTimezone.getFullYear(),
    hours: userDateInTimezone.getHours(),
    minutes: userDateInTimezone.getMinutes(),
    seconds: userDateInTimezone.getSeconds(),
    start_interval_time: start_time,
    end_interval_time: end_time,
  };
    
  const userAttributes = {
    set_attributes: dateObject
  };
  
  response.json(userAttributes);
});


module.exports = router;
