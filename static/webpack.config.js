const webpack = require("webpack");
const CompressionPlugin = require("compression-webpack-plugin");

const config = {
  entry: {
    login: __dirname + "/js/login.jsx",
    admin: __dirname + "/js/adminPanel.jsx",
    index: __dirname + "/js/index.jsx",
    fileUpload: __dirname + "/js/fileUpload.jsx"
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
      },
      {
        test: /\.(woff|woff2|eot|ttf)$/,
        loader: "url-loader?limit=100000"
      },
      {
        test: /\.(png|svg|jpg|gif)$/,
        use: ["file-loader"]
      },
      {
        test: /\.(sass|scss)$/,
        include: /index/,
        use: [
          { loader: "style-loader" },
          { loader: "css-loader", options: { modules: false } },
          { loader: "sass-loader" }
        ]
      },
      {
        test: /\.(sass|scss)$/,
        exclude: /index/,
        use: [
          { loader: "style-loader" },
          { loader: "css-loader", options: { modules: true } },
          { loader: "sass-loader" }
        ]
      }
    ]
  }
};
// module.exports = {
//     "plugins" = new CompressionPlugin;
// }
module.exports = config;
