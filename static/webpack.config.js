const webpack = require("webpack");

const config = {
  entry: {
    index: __dirname + "/js/index.jsx",
    fileUpload: __dirname + "/js/fileUpload.jsx",
    report: __dirname + "/js/index.jsx"
  },
  output: {
    path: __dirname + "/dist",
    filename: "[name].js"
  },
  resolve: {
    extensions: [".js", ".jsx", ".css"]
  },
  module: {
    rules: [
      {
        test: /\.jsx?/,
        exclude: /node_modules/,
        use: "babel-loader"
      },
      {
        test: /\.css$/,
        loader: ["style-loader", "css-loader"]
      }
    ]
  }
};
module.exports = config;
