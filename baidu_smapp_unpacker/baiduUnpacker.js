const path = require("path");
const UglifyJS = require("uglify-es");
const {js_beautify} = require("js-beautify").js;
const beautify_html = require('js-beautify').html;
const {VM} = require('vm2');
const fs = require("fs")
const glob = require("glob");
const reg = /(?<=").*?(?=")/;
const csv = require('csv-parser');
// const myTraverse = require('./myTraverse')
const jsdom = require("jsdom");
const {JSDOM} = jsdom;
const fse = require('fs-extra');


const configContent = fs.readFileSync('../config.ini', 'utf-8');
// 使用正则表达式匹配dec_dir的值
const match = configContent.match(/^dec_dir\s*=\s*(.*)$/m);
const match_2 = configContent.match(/^miniapp_dict\s*=\s*(.*)$/m);
if (!match) {
    throw new Error('Failed to read dec_dir from config.ini');
}
const decDir = match[1];
const miniappDir = match_2[1];


function jsBeautify(code) {
    return UglifyJS.minify(code, {mangle: false, compress: false, output: {beautify: true, comments: true}}).code;
  }
  
  function swanBeautify(code) {
    return beautify_html(code, {indent_size: 2, space_in_empty_paren: true});
  }
  

  const parser = require('@babel/parser')
  const t = require('@babel/types')
  const traverse = require('@babel/traverse').default
  const generate = require('@babel/generator').default
  
  function myTraverse(code) {
    const MyVisitor = {
      FunctionDeclaration(path) {
        const paraMap = {
          "params.0": "require",
          "params.1": "module",
          "params.2": "exports",
          "params.3": "define",
          "params.4": "swan",
          "params.5": "getApp",
        }
        for (let key in paraMap) {
          const paramOldName = path.get(key)
          if (!paramOldName){
            continue
          }
          const paramNewName = paraMap[key]
          path.scope.rename(paramOldName.node.name, paramNewName)
        }
        path.stop();
      }
    }
    let ast = parser.parse(code);
    traverse(ast, MyVisitor);
    const output = generate(ast, {}, code);
    return output.code;
  }
  
  module.exports = {myTraverse: myTraverse};
  if (require.main === module) {
  
    // let code = `function square(n) {
    //   return n * n;
    // }`
    let code = `
    function temp(n, e, t, o, i, a, s, r, u, d, c, l, g, _, m, p, b, f, w, h, I, v, x) {
    "use strict";
  
    
      Page({
        data: {
          userInfo: {},
          hasUserInfo: !1,
          canIUse: i.canIUse("button.open-type.getUserInfo")
        },
        onLoad: function () {},
        getUserInfo: function (n) {
          this.setData({
            userInfo: n.detail.userInfo,
            hasUserInfo: !0
          }), console.log(t(10));
        },
        navigateToSecondPage: function () {
          i.navigateTo({
            url: "/pages/page2/page2"
          });
        },
        navigateToDynamic: function () {
          i.navigateTo({
            url: "/pages/page3/page3"
          });
        },
        navigateToSubpackage: function () {
          console.log("dddd"), i.navigateTo({
            url: "/subpackage/pages/index/index"
          });
        }
      });
  
  };
  `
    code = myTraverse(code);
    console.log(code);
  }
  
  function getHeadString(char) {
    let s = 'e.global, e.Function, e.setTimeout, e.setInterval, e.setImmediate, e.requestAnimationFrame, e.swanGlobal, e.jsNative, e.masterManager, e._openSourceDebugInfo, e.System, e.Bdbox_aiapps_jsbridge, e.Bdbox_android_jsbridge, e.Bdbox_android_utils, e._naFile, e._naInteraction, e._naNetwork, e._naRouter, e._naSetting, e._naStorage, e._naUtils, e.globalThis;'
    s = s.replace(/e\./g, char + '.');
    return s;
  }
  
  function getId2Name(content) {
    // TODO 正则和window.__swanRoute="app" 需要使用同样的引号
    // const s = content.substring(content.indexOf('window.__swanRoute=\'app\''))
    const s = content.substring(content.indexOf('window.__swanRoute="app"'))
  
    // console.log(s);
  
    const fileNameReg = /window.__swanRoute="(.*?)"/g;
    const fileNames = s.match(fileNameReg);
    const fileIdReg = /require\("(.*?)"\)/g;
    const fileIds = s.match(fileIdReg);
  
    const fileId2Name = {}
    console.assert(fileNames.length === fileIds.length, 'cannot get file id and name mapping');
  
    let i = 0
    for (; i < fileNames.length; i++) {
      fileId2Name[reg.exec(fileIds[i])] = reg.exec(fileNames[i])[0]
    }
  
    // console.log('[Unpacking Project File] total js files:' + i);
    // console.log(fileId2Name);
    return fileId2Name
  }
  
  
  /*
  * 针对createPage，通过括号匹配的方式，提取page对应的定义
  * */
  function getEndIndex(code) {
    let str = '';
    const stack = [];
    for (let i = 0; i < code.length; i++) {
      const letter = code[i];
      str += letter;
  
      if (letter === '(') {
        stack.push(code[i]);
      } else if (letter === ')') {
        if (stack[stack.length - 1] === '(') {
          stack.splice(-1, 1);
          if (stack.length === 0) {
            return str;
          }
        } else {
          stack.push(letter)
        }
      }
    }
    throw 'can not find page or component definition'
  }
  
  function checkCreatePageOrComponent(code) {
    if (code.indexOf('createPage)({') > -1) {
      code = 'Page' + code.slice(code.indexOf("createPage)") + 11).trim();
      code = getEndIndex(code)
    } else if (code.indexOf('createComponent)({') > -1) {
      code = 'Component' + code.slice(code.indexOf("createComponent)") + 16).trim();
      code = getEndIndex(code)
    }
    return code;
  }
  
  
  function storeFile(filepath, code) {
    if (!fs.existsSync(path.dirname(filepath))) {
      fs.mkdirSync(path.dirname(filepath), {recursive: true});
    }
    try {
      fs.writeFileSync(filepath, code);
    } catch (e) {
      console.log(e)
      console.log(`save ${filepath} fail`);
    }
  }
  
  function unpackJs(root, appJsPath) {
    if (!fs.existsSync(appJsPath)) {
      throw 'can not find app.js'
    }
    const content = fs.readFileSync(appJsPath).toString();
    const fileId2Name = getId2Name(content);
    const start = `
      var define ;
      var window = window || {
          define : define
      };
      var define = window.define;
      var setTimeout = setTimeout || {};
      var setInterval = setInterval || {};
      var setImmediate = setImmediate || {};
      var eval = eval || {};
      var requestAnimationFrame = requestAnimationFrame || {};`
  
    const codestring = start + jsBeautify(content);
  
    const sandbox = {
      require() {
      },
      define(fileId, func) {
        let filename = fileId2Name[fileId.toString()];
        // some js file just know its id, but can not get its file path
        if (filename === undefined) {
          filename = fileId;
        }
  
        let code = func.toString();
        //storeFile(path.join(root, filename + '-temp.js'), code);
        code = myTraverse('function temp ' + code.slice(8));
  
        code = code.slice(code.indexOf("{") + 1, code.lastIndexOf("}") - 1).trim();
        if (code.startsWith('"use strict";')) {
          code = code.substring(13).trim();
        }
        if (code.startsWith('!function')) {
          code = code.slice(code.indexOf("{") + 1, code.lastIndexOf("}") - 1).trim();
          try {
            const arugment = code.match(/\([a-z]\)/)[0][1]
            code = code.replace(getHeadString(arugment), '').trim();
          }catch (e) {
  
          }
        }
        code = checkCreatePageOrComponent(code);
  
        storeFile(path.join(root, filename + '.js'), code);
      },
    }
    const vm = new VM({sandbox: sandbox});
    vm.run(codestring);
  }
  
  function unpackSubPackage(root) {
    const content = JSON.parse(fs.readFileSync(path.join(root, './app.json')).toString());
    const subPackages = content['subPackages'];
    if (subPackages) {
      console.log(`total subPackage: ${subPackages.length}`)
      let unpackNum = 0;
      for (const sub of subPackages) {
        const subDir = sub['root'];
        const subAppJsPath = path.resolve(root, subDir, './app.js');
        try {
          unpackJs(root, subAppJsPath);
          console.log(`[unpack subPackage] ${subDir} success`)
          unpackNum = unpackNum + 1;
        } catch (e) {
          console.log(`[unpack subPackage] can not find ${subDir} app.js`)
        }
      }
      console.log(`unpack subPackage success: ${unpackNum}`)
    }
  }

  function unpackSwan(dir) {
    const getDirectories = function (src, callback) {
      // TODO allCusomComponents 这类型不能直接解析
      glob(src + '/**/*.swan.js', callback);
    };
    getDirectories(dir, function (err, res) {
      if (err) {
        console.log('Error', err);
      } else {
        res.forEach(file => {
          const content = fs.readFileSync(file).toString();
          const start = content.indexOf('template:') + 10;
          const end = content.indexOf(',isComponent:') - 1;
          let swan = content.substring(start, end);
          swan = swan.replace(/\\\'/g, '\'');
          swan = swan.replace(/\\\"/g, '"');
          swan = dealEvent(swan);
          swan = swanBeautify(swan);
  
          const filepath = file.substring(0, file.lastIndexOf('.js'));
          fs.writeFile(filepath, swan, (err) => {
            if (err) {
              console.log(`save ${filepath} fail`);
            } else {
              // console.log(`save ${filepath} success`)
              fs.rmSync(file);
            }
          });
        })
      }
    });
  
    function dealEvent(swan) {
      let dom = new JSDOM(swan);
      // console.log(dom.window.document.body.textContent)
      Array.from(dom.window.document.body.getElementsByTagName("*")).forEach(element => {
        Array.from(element.attributes).forEach(attribute => {
          try {
            if (attribute.name.startsWith('on-bind')) {
              let event = attribute.name.toString().substring(3);
              let handler = attribute.value.toString().split(',')[2].trim();
              element.setAttribute(event, handler);
              element.removeAttribute(attribute.name);
            }
          } catch (e) {
            console.log(e);
          }
        })
      });
      return dom.window.document.documentElement.outerHTML
    }
  }
  
// function unpackPkg(packageName) {
//   // const sourceDir = path.join('D:\\baidu-mini-program(no unpack)\\', packageName);
//   /* E:\baidu_miniapp\autoxjs_script\sync_smapp_dir\aiapps_folder */
//   const sourceDir = path.join('E:\\baidu_miniapp\\autoxjs_script\\sync_smapp_dir\\aiapps_folder\\', packageName);
//   console.log(`unpacking ${sourceDir}`);
//   const directories = fs.readdirSync(sourceDir);
//   if (directories.length > 1) {
//     throw 'find more than one version of the mini program!';
//   }
//   const targetDir = path.join('D:\\baidu-mini-program', packageName)
//   if (fs.existsSync(targetDir)){
//     fs.rmdirSync(targetDir,{recursive:true});
//   }
//   fse.copySync(sourceDir, targetDir)

//   const root = path.join(targetDir, directories[0]);
//   try {
//     unpackJs(root, path.join(root, 'app.js'));
//     unpackSwan(root);
//     console.log(`[unpack masterPackage] success`)
//     unpackSubPackage(root);
//     console.log(`unpack ${root} success`)
//   } catch (e) {
//     console.log(e)
//     console.log(`unpack ${root} fail`)
//   }
// }

function unpackPkg(packageName) {
  // 使用dec_dir来替换原有的路径
  const sourceDir = path.join(miniappDir, packageName);
  console.log(`unpacking ${sourceDir}`);

  const directories = fs.readdirSync(sourceDir);
  if (directories.length > 1) {
    throw 'find more than one version of the mini program!';
  }

  // targetDir修改为dec_dir + packageName + "_dec"
  const targetDir = path.join(decDir, packageName + "_dec");
  if (fs.existsSync(targetDir)){
    fs.rmdirSync(targetDir,{recursive:true});
  }
  fse.copySync(sourceDir, targetDir)

  const root = path.join(targetDir, directories[0]);
  try {
    unpackJs(root, path.join(root, 'app.js'));
    unpackSwan(root);
    console.log(`[unpack masterPackage] success`)
    unpackSubPackage(root);
    console.log(`unpack ${root} success`)
  } catch (e) {
    console.log(e)
    console.log(`unpack ${root} fail`)
  }
}

function run() {
  unpackPkg(process.argv[2]);
}

module.exports = {run: run};
if (require.main === module) {
  run();
}



