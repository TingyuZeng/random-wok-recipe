"use strict";

var width, height;
var pixels = [];
var coloredPixels = [];
var colors = ['#540045', '#C60052', '#FF714B', '#EAFF87', '#ACFFE9'];
var currentPixel = 0;
var mousePosition = {
  x: window.innerWidth / 2,
  y: window.innerHeight / 2
};
var canvas = document.getElementById('canvas');
var ctx = canvas.getContext('2d');

var drawGrid = function drawGrid() {
  ctx.clearRect(0, 0, width, height);

  for (var i = 0, l = pixels.length; i < l; i++) {
    pixels[i][4] = 0;
  }

  for (var _i = 0, _l = coloredPixels.length; _i < _l; _i++) {
    var pix = Math.floor(coloredPixels[_i].y / 10) * (Math.floor(width / 10) + 1) + Math.floor(coloredPixels[_i].x / 10);

    if (pixels[pix]) {
      pixels[pix][4] = coloredPixels[_i].color;
      pixels[pix][5] = coloredPixels[_i].alpha;
    }

    if (coloredPixels[_i].alpha > 0) coloredPixels[_i].alpha -= 0.008;
    if (coloredPixels[_i].alpha < 0) coloredPixels[_i].alpha = 0;
    coloredPixels[_i].x += coloredPixels[_i].vx;
    coloredPixels[_i].y += coloredPixels[_i].vy;
  }

  for (var _i2 = 0, _l2 = pixels.length; _i2 < _l2; _i2++) {
    ctx.globalAlpha = 1;
    ctx.fillStyle = '#222';
    ctx.fillRect(pixels[_i2][0], pixels[_i2][1], pixels[_i2][2], pixels[_i2][3]);
    ctx.globalAlpha = pixels[_i2][5];
    ctx.fillStyle = pixels[_i2][4];
    ctx.fillRect(pixels[_i2][0], pixels[_i2][1], pixels[_i2][2], pixels[_i2][3]);
  }
};

var resize = function resize() {
  width = window.innerWidth;
  height = window.innerHeight;
  canvas.width = width;
  canvas.height = height;
  pixels = [];

  for (var y = 0; y < height / 10; y++) {
    for (var x = 0; x < width / 10; x++) {
      pixels.push([x * 10, y * 10, 8, 8, '#222', 1]);
    }
  }
};

var draw = function draw() {
  launchPixel();
  launchPixel();
  drawGrid();
  requestAnimationFrame(draw);
};

var initColoredPixels = function initColoredPixels() {
  for (var i = 0; i < 300; i++) {
    coloredPixels.push({
      x: width / 2,
      y: height / 2,
      alpha: 0,
      color: colors[i % 5],
      vx: -1 + Math.random() * 2,
      vy: -1 + Math.random() * 2
    });
  }
};

var launchPixel = function launchPixel() {
  coloredPixels[currentPixel].x = mousePosition.x;
  coloredPixels[currentPixel].y = mousePosition.y;
  coloredPixels[currentPixel].alpha = 1;
  currentPixel++;
  if (currentPixel > 299) currentPixel = 0;
};

resize();
initColoredPixels();
draw();
window.addEventListener('resize', resize);
window.addEventListener('mousemove', function (e) {
  mousePosition.x = e.pageX;
  mousePosition.y = e.pageY;
});

var touchMove = function touchMove(e) {
  e.preventDefault();
  mousePosition.x = e.touches[0].pageX;
  mousePosition.y = e.touches[0].pageY;
};

document.addEventListener('touchstart', touchMove);
document.addEventListener('touchmove', touchMove);