/**
* Template Name: Maundy - v4.6.0
* Template URL: https://bootstrapmade.com/maundy-free-coming-soon-bootstrap-theme/
* Author: BootstrapMade.com
* License: https://bootstrapmade.com/license/
*/
(function() {
  
  
  "use strict";

  /**
   * Easy selector helper function
   */
  const select = (el, all = false) => {
    el = el.trim()
    if (all) {
      return [...document.querySelectorAll(el)]
    } else {
      return document.querySelector(el)
    }
  }

  /**
   * Easy event listener function
   */
  const on = (type, el, listener, all = false) => {
    let selectEl = select(el, all)
    if (selectEl) {
      if (all) {
        selectEl.forEach(e => e.addEventListener(type, listener))
      } else {
        selectEl.addEventListener(type, listener)
      }
    }
  }

  /**
   * Easy on scroll event listener 
   */
  const onscroll = (el, listener) => {
    el.addEventListener('scroll', listener)
  }

  /**
   * Back to top button
   */
  let backtotop = select('.back-to-top')
  if (backtotop) {
    const toggleBacktotop = () => {
      if (window.scrollY > 100) {
        backtotop.classList.add('active')
      } else {
        backtotop.classList.remove('active')
      }
    }
    window.addEventListener('load', toggleBacktotop)
    onscroll(document, toggleBacktotop)
  }

  /**
   * Countdown timer
   */
  let countdown = select('.countdown');
  // const output = countdown.innerHTML;

  const countDownDate = function() {
    let timeleft = new Date(countdown.getAttribute('data-count')).getTime() - new Date().getTime();

    let days = Math.floor(timeleft / (1000 * 60 * 60 * 24));
    let hours = Math.floor((timeleft % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
    let minutes = Math.floor((timeleft % (1000 * 60 * 60)) / (1000 * 60));
    let seconds = Math.floor((timeleft % (1000 * 60)) / 1000);

    countdown.innerHTML = output.replace('%d', days).replace('%h', hours).replace('%m', minutes).replace('%s', seconds);
  }
  // countDownDate();
  // setInterval(countDownDate, 1000);

})()

function set_http(){
  document.getElementById("http-button").innerText = "http://"
}

function set_https(){
  document.getElementById("http-button").innerText = "https://"
}

async function create_new_url() {
  var entered_short_url= document.getElementById("short-url-input").value;
  var entered_url = document.getElementById("original-url-input").value;
  var entered_url_prefix = document.getElementById("http-button").innerText;

  let request_body = {
    "original_url" : entered_url_prefix + entered_url
  };
  
  if (entered_short_url) {
    request_body["short_url"] = entered_short_url;
  }
  

  let response = await fetch(
    "http://localhost:5002/new",{
      method: "POST",
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(request_body)
    }
  );
  console.log(response.json())

  await getData();
}

async function getData() {
  console.log("Get data function");
  const response = await fetch("http://localhost:5002/all");
  const database = await response.json();
  // console.log(database.data[1].id);
  const {code, data} = database;
  // console.log(data[1]);

  var table = document.getElementById("existing-url-table");

  let table_html = `            
  <tr>
    <th>Shortened URL</th>
    <th>Original URL</th>
  </tr>
  `;

  // add json data to table as rows 
  for (var i = 0; i < data.length; i++){
    console.log(data[i].original_url);

    current_original_url = data[i]["original_url"];
    current_shortened_url = document.getElementById("short-url-input-addon").innerText + data[i]["short_url"];

    current_html = `
    <tr>
      <td> 
        <a target="_blank" href="${current_shortened_url}" class="link-primary">${current_shortened_url}</a> 
      </td>
      <td>
        <a target="_blank" href="${current_original_url}" class="link-secondary">${current_original_url}</a> 
      </td>
    </tr>
    `;

    table_html += current_html;
  }

  // update table
  table.innerHTML = table_html;
  // console.log(typeof(table))
}