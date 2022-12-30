 async function fetchData(){
  const response = await fetch('https://api.npoint.io/5deec383d686ac3c0486');
  const data = await response.json();
  console.log(data);

 }
 fetchData()

 var images = ['image1.jpg', 'image2.jpg', 'image3.jpg'];
      var index = 0;

      document.getElementById('button--a').onclick = function() {

      }