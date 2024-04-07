// Import the functions you need from the SDKs you need
// Initialize Firebase
firebase.initializeApp({
  apiKey: "AIzaSyAcbwVFge8wF_lvzP6cfiVsvZIy9AiZNEI",
  authDomain: "ehsan-d211b.firebaseapp.com",
  projectId: "ehsan-d211b",
  storageBucket: "ehsan-d211b.appspot.com",
  messagingSenderId: "221541812002",
  appId: "1:221541812002:web:1c9b656bce39778220877b",
});

const messaging = firebase.messaging();
console.log("It is connected");

// Check that service workers are supported
// if ("serviceWorker" in navigator) {
//   // Use the window load event to keep the page load performant
//   window.addEventListener("load", () => {
//     navigator.serviceWorker.register("/firebase-messaging-sw.js");
//   });
// }    
// onMessage((payload) => {
//   console.log("Message received. ", payload);
//   // Customize notification here
//   const notificationTitle = payload.data.title;
//   const notificationOptions = {
//     body: payload.data.body,
//     icon: payload.data.icon_url,
//   };

//   return self.registration.showNotification(
//     notificationTitle,
//     notificationOptions
//   );
// });
messaging.onMessage((payload) => {
  console.log('Message received. ', payload);
  // ...
});
