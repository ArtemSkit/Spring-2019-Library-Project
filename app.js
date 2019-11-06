/******************************************************************************
 * Program     : app.js
 * Author      : Artem Skitenko
 * Date        : Spring 2019
 * Description : This application acts as an intermediary between a custom 
 *               Flask Microservice and Google Services. This "handler" takes
 *               in POST requests from Google Services and passes queries to
 *               the backend Flask App. In this case, queries on San Antonio
 *               Public Library account information such as 'What items are
 *               on hold?' to 'What items do I have checked out?'
 *****************************************************************************/

/* Modules Required */
const express = require('express');
const bodyParser = require('body-parser');
const fetch = require('node-fetch')
const cheerio = require('cheerio')
const axios = require('axios')
const { Card } = require('dialogflow-fulfillment');
//const functions = require('firebase-functions') // No longer in use

/* Modules Used by Google Actions */
const {
  dialogflow,
  actionssdk,
  Image,
  Table,
  Carousel,
  SimpleResponse,
  BasicCard
} = require('actions-on-google');
const app = dialogflow({
  clientId: "919110839943-XXXXXXXXXX.apps.googleusercontent.com",
  debug: true
});


/* Google Intent for Items Checked Out */
app.intent('Items_Checked_Out', (conv) => {
  console.log(conv.user.id);
  return axios.get('http://localhost:5000/items').then(data => {
    myData = data.data.Data;
    conv.add('You have ' + myData.length + ' items checked out.  \n');
    var rows = []
    console.log(myData)
    for (let index = 0; index < myData.length; index++) {
      rows.push([myData[index].title, myData[index].status])
    }
    if (myData.length > 0) {
      conv.add(new Table({
        dividers: true,
        columns: ['Title', 'Status'],
        rows: rows,
      }))
    }
    // conv.add(myData);
    conv.ask('What else can I do for you?');
  }).catch(error => {
    console.log(error)
  })
});

/* Google Intent for Items on Hold */
app.intent('Items_On_Hold', (conv) => {
  console.log(conv.user.id);
  return axios.get('http://localhost:5000/holds').then(data => {
    myData = data.data.Data;
    conv.add('You have ' + myData.length + ' items on hold.  \n');
    var rows = []
    console.log(myData)
    for (let index = 0; index < myData.length; index++) {
      rows.push([myData[index].title, myData[index].status])
    }
    if (myData.length > 0) {
      conv.add(new Table({
        dividers: true,
        columns: ['Title', 'Status'],
        rows: rows,
      }))
    }
    // conv.add(myData);
    conv.ask('What else can I do for you?');
  }).catch(error => {
    console.log(error)
  })
});

/* Parse into JSON format */
const expressApp = express().use(bodyParser.json());

/* ExpressJS Post Handler and Socket */
expressApp.post('/app', app);
expressApp.listen(3000, "127.0.0.1");
