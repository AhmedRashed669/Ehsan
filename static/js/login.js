import { initializeApp } from "https://www.gstatic.com/firebasejs/10.10.0/firebase-app.js";
import {
  getMessaging,
  getToken,
} from "https://www.gstatic.com/firebasejs/10.10.0/firebase-messaging.js";

let currentToken = null;

// a function to get the csrf token for the post request of send token function
function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
      const cookies = document.cookie.split(';');
      for (let i = 0; i < cookies.length; i++) {
          const cookie = cookies[i].trim();
          // Does this cookie string begin with the name we want?
          if (cookie.substring(0, name.length + 1) === (name + '=')) {
              cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
              break;
          }
      }
  }
  return cookieValue;
}

const checkPermission = () => {
  if (!('serviceWorker' in navigator)) {
      throw new Error("No support for service worker!")
  }

  if (!('Notification' in window)) {
      throw new Error("No support for notification API");
  }

  if (!('PushManager' in window)) {
      throw new Error("No support for Push API")
  }
}

const requestNotificationPermission = async () => {
  const permission = await Notification.requestPermission();

  if (permission !== 'granted') {
      throw new Error("Notification permission not granted")
  }
  else{
     getToken(messaging, {
      vapidKey:
        "BKYFe1K0zc62r5PgdTtkYZySqp-yRaFU4p0g8Fsr-a9HM-WAzeoRvu2cZzeJGx-eOeqLJjyOF4GclAfeIpZyqQc",
    })
      .then((token) => {
        if (token) {
          // Send the token to your server and update the UI if necessary
          // ...
          currentToken = token;
        } else {
          // Show permission request UI
          console.log(
            "No registration token available. Request permission to generate one."
          );
          // ...
        }
      })
      .catch((err) => {
        console.log("An error occurred while retrieving token. ", err);
        // ...
      });
  }
}

// TODO: Add SDKs for Firebase products that you want to use
// https://firebase.google.com/docs/web/setup#available-libraries
// Your web app's Firebase configuration
const firebaseConfig = {
  apiKey: "AIzaSyAcbwVFge8wF_lvzP6cfiVsvZIy9AiZNEI",
  authDomain: "ehsan-d211b.firebaseapp.com",
  projectId: "ehsan-d211b",
  storageBucket: "ehsan-d211b.appspot.com",
  messagingSenderId: "221541812002",
  appId: "1:221541812002:web:1c9b656bce39778220877b",
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const messaging = getMessaging(app);

//sending data to login view in django
const sendData = () => {
  // Get the username and password from the form
  const usernameField = document.querySelector("#id_username");
  const passwordField = document.querySelector("#id_password");
  const csrftoken = getCookie('csrftoken');

  axios
    .post(
      "https://ehsandonorsys.pythonanywhere.com/accounts/login/",
      {
        username: usernameField.value,
        password: passwordField.value,
      },
      {
        withCredentials: true,
        headers: {
          "Content-Type": "application/x-www-form-urlencoded", // Change the Content-Type
          "X-CSRFTOKEN": csrftoken,
        },
      }
    )
    .then((response) => {
      console.log("Received response: ", response.data); // Print received response
      if (response.data["message"] === true) {
        console.log(currentToken);
        sendToken(currentToken);
        window.location.replace("https://ehsandonorsys.pythonanywhere.com/patients/");
      } else {
        // Set the fields to null
        usernameField.value = "";
        passwordField.value = "";
        alert("Wrong Credentials");
      }
    });
};

// sending token to the server
const sendToken = (currentToken) => {
  const csrftoken = getCookie('csrftoken');
  axios({
    method: 'post',
    url: 'https://ehsandonorsys.pythonanywhere.com/api/fcmdevices/',
    headers: {'X-CSRFToken': csrftoken},
    data: {
      'registration_id': currentToken,
      'type': 'web'
    }
  })
  .then(function (response) {
    console.log(response);
  })
  .catch(function (error) {
    console.log(error);
  });
};


const signbutton = document
  .querySelector("#sign")
  .addEventListener("click", sendData);


const registerSW = async () => {
  const registration = await navigator.serviceWorker.register('/firebase-messaging-sw.js');
  console.log("registered");
  return registration;
}

const main = async () => {
  checkPermission()
  await requestNotificationPermission();
  const reg = await registerSW();
  reg.showNotification("hello world")
}
main()
// on local host uncomment this
// Import the functions you need from the SDKs you need
// import { initializeApp } from "https://www.gstatic.com/firebasejs/10.10.0/firebase-app.js";
// import {
//   getMessaging,
//   getToken,
// } from "https://www.gstatic.com/firebasejs/10.10.0/firebase-messaging.js";

// let currentToken = null;

// // a function to get the csrf token for the post request of send token function
// function getCookie(name) {
//   let cookieValue = null;
//   if (document.cookie && document.cookie !== '') {
//       const cookies = document.cookie.split(';');
//       for (let i = 0; i < cookies.length; i++) {
//           const cookie = cookies[i].trim();
//           // Does this cookie string begin with the name we want?
//           if (cookie.substring(0, name.length + 1) === (name + '=')) {
//               cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
//               break;
//           }
//       }
//   }
//   return cookieValue;
// }

// const checkPermission = () => {
//   if (!('serviceWorker' in navigator)) {
//       throw new Error("No support for service worker!")
//   }

//   if (!('Notification' in window)) {
//       throw new Error("No support for notification API");
//   }

//   if (!('PushManager' in window)) {
//       throw new Error("No support for Push API")
//   }
// }

// const requestNotificationPermission = async () => {
//   const permission = await Notification.requestPermission();

//   if (permission !== 'granted') {
//       throw new Error("Notification permission not granted")
//   }
//   else{
//      getToken(messaging, {
//       vapidKey:
//         "BKYFe1K0zc62r5PgdTtkYZySqp-yRaFU4p0g8Fsr-a9HM-WAzeoRvu2cZzeJGx-eOeqLJjyOF4GclAfeIpZyqQc",
//     })
//       .then((token) => {
//         if (token) {
//           // Send the token to your server and update the UI if necessary
//           // ...
//           currentToken = token;
//         } else {
//           // Show permission request UI
//           console.log(
//             "No registration token available. Request permission to generate one."
//           );
//           // ...
//         }
//       })
//       .catch((err) => {
//         console.log("An error occurred while retrieving token. ", err);
//         // ...
//       });
//   }
// }

// // TODO: Add SDKs for Firebase products that you want to use
// // https://firebase.google.com/docs/web/setup#available-libraries
// // Your web app's Firebase configuration
// const firebaseConfig = {
//   apiKey: "AIzaSyAcbwVFge8wF_lvzP6cfiVsvZIy9AiZNEI",
//   authDomain: "ehsan-d211b.firebaseapp.com",
//   projectId: "ehsan-d211b",
//   storageBucket: "ehsan-d211b.appspot.com",
//   messagingSenderId: "221541812002",
//   appId: "1:221541812002:web:1c9b656bce39778220877b",
// };

// // Initialize Firebase
// const app = initializeApp(firebaseConfig);
// const messaging = getMessaging(app);

// //sending data to login view in django
// const sendData = () => {
//   // Get the username and password from the form
//   const usernameField = document.querySelector("#id_username");
//   const passwordField = document.querySelector("#id_password");
//   const csrftoken = getCookie('csrftoken');

//   axios
//     .post(
//       "http://127.0.0.1:8000/accounts/login/",
//       {
//         username: usernameField.value,
//         password: passwordField.value,
//       },
//       {
//         withCredentials: true,
//         headers: {
//           "Content-Type": "application/x-www-form-urlencoded", // Change the Content-Type
//           "X-CSRFTOKEN": csrftoken,
//         },
//       }
//     )
//     .then((response) => {
//       console.log("Received response: ", response.data); // Print received response
//       if (response.data["message"] === true) {
//         console.log(currentToken);
//         sendToken(currentToken);
//         window.location.replace("http://127.0.0.1:8000/patients/");
//       } else {
//         // Set the fields to null
//         usernameField.value = "";
//         passwordField.value = "";
//         alert("Wrong Credentials");
//       }
//     });
// };

// // sending token to the server
// const sendToken = (currentToken) => {
//   const csrftoken = getCookie('csrftoken');
//   axios({
//     method: 'post',
//     url: 'http://127.0.0.1:8000/api/fcmdevices/',
//     headers: {'X-CSRFToken': csrftoken},
//     data: {
//       'registration_id': currentToken,
//       'type': 'web'
//     }
//   })
//   .then(function (response) {
//     console.log(response);
//   })
//   .catch(function (error) {
//     console.log(error);
//   });
// };


// const signbutton = document
//   .querySelector("#sign")
//   .addEventListener("click", sendData);


// const registerSW = async () => {
//   const registration = await navigator.serviceWorker.register('/firebase-messaging-sw.js');
//   console.log("registered");
//   return registration;
// }

// const main = async () => {
//   checkPermission()
//   await requestNotificationPermission();
//   const reg = await registerSW();
//   reg.showNotification("hello world")
// }
// main()