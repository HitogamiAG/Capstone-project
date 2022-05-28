let video = document.getElementById("video");
let model;
let asd = document.getElementById("fer_model_js");

const setupCamera = () => {
    navigator.mediaDevices
      .getUserMedia({
        video: { width: 600, height: 400 },
        audio: false,
      })
      .then((stream) => {
        video.srcObject = stream;
      });
  };

  const detectFaces = async () => {
    const prediction = await model.estimateFaces(video, false);

    let imageTensor = tf.browser.fromPixels(video);
    const offset = tf.scalar(255.0);
    const normalized = imageTensor.div(offset);
    const batched = normalized.expandDims(0);
    let result = batched;

    const size = 224;
    const height = imageTensor.shape[0];
    const width = imageTensor.shape[1];
    const imgSize = Math.min(width, height);
    const left = (width - imgSize) / 2;
    const top = (height - imgSize) / 2;
    const right = (width + imgSize) / 2;
    const bottom = (height + imgSize) / 2;
    let boxes = [[top / height, left / width, bottom / height, right / width]];
    result = tf.image.cropAndResize(batched, boxes, [0], [size,size]);
    
    const squezed = tf.squeeze(result);
    const x1 = tf.slice(squezed, [0, 0 ,0], [1, 3, 3]).sub(103.939);
    const x2 = tf.slice(squezed, [1, 0 ,0], [1, 3, 3]).sub(116.779);
    const x3 = tf.slice(squezed, [2, 0 ,0], [1, 3, 3]).sub(123.68);
    let t3 = tf.concat([x1.dataSync(), x2.dataSync(), x3.dataSync()], 0);
    const ready_to_predict = tf.tensor4d(tf.concat([x1.dataSync(), x2.dataSync(), x3.dataSync()], 0).dataSync(), [1, 3, 3 ,3]);
    
    console.log(fer_model);
    
  }

  setupCamera();
  video.addEventListener("loadeddata", async () => {
    model = await blazeface.load();
    // call detect faces every 100 milliseconds or 10 times every second
    setInterval(detectFaces, 1000);
  });