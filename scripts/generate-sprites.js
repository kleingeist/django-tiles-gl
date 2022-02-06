const yargs = require("yargs/yargs");
const { hideBin } = require("yargs/helpers");
const spritezero = require("@mapbox/spritezero");
const fs = require("fs");
const glob = require("glob");
const path = require("path");

const argv = yargs(hideBin(process.argv)).command(
  "$0 <inputDirectory> <outputDirectory>"
).argv;

const pixelRatios = [1, 2];

// if (!fs.existsSync(argv.outputDirectory)) {
//     fs.mkdirSync(argv.outputDirectory)
// }

const svgs = glob
  .sync(path.resolve(path.join(argv.inputDirectory, "*.svg")))
  .map((file) => ({
    svg: fs.readFileSync(file),
    id: path.basename(file).replace(".svg", ""),
  }));

pixelRatios.forEach((pixelRatio) => {
  const baseName = pixelRatio != 1 ? `sprite@${pixelRatio}x` : "sprite";
  const pngPath = path.join(argv.outputDirectory, `${baseName}.png`);
  const jsonPath = path.join(argv.outputDirectory, `${baseName}.json`);

  spritezero.generateLayout(
    { imgs: svgs, pixelRatio: pixelRatio, format: true },
    function (err, dataLayout) {
      if (err) {
        console.error(err);
      } else {
        fs.writeFileSync(jsonPath, JSON.stringify(dataLayout));
      }
    }
  );

  spritezero.generateLayout(
    { imgs: svgs, pixelRatio: pixelRatio, format: false },
    function (err, imageLayout) {
      spritezero.generateImage(imageLayout, function (err, image) {
        if (err) {
          console.error(err);
        } else {
          fs.writeFileSync(pngPath, image);
        }
      });
    }
  );
});
