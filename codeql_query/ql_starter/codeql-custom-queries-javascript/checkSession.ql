import javascript
import DataFlow

/**
 * @name miniCSRF_Check_session
 * @id mini_csrf_session
 * @kind problem
 * @problem.severity warning
 */


string sessionCheck(){
    result = "%.checkSession"
    or
    result = "%.getStorage"
    or
    result = "%.getStorageInfo" 
    or
    result = "%.getStorageInfoSync"
    or
    result = "%.getStorageSync"
}

string pageFunction(){
  result = "onLoad"
  or 
  result = "onShow"
  or
  result = "onLaunch"
  or
  result = "onReady"
}

private DataFlow::InvokeNode wx_session() { result.getCalleeNode().toString().matches(sessionCheck()) }


// class SessionCheck extends TaintTracking::Configuration {
//   SessionCheck() { this = "check session" }

//   override predicate isSource(DataFlow::Node source) { 
//     any()
//   }


//   override predicate isSink(DataFlow::Node sink) {

//     wx_session().(DataFlow::Node) = sink

//   }

// }


// query predicate session_check(
//     DataFlow::Node sink, string container_name,File session_file_path
//     //ControlFlowNode source_func
//     ){
//     exists(
//       SessionCheck pt,DataFlow::Node source| 
//       pt.hasFlow(source, sink)|
//       container_name = sink.getContainer().(Function).getName()
//       and
//       container_name.matches(pageFunction())
//       and
//       session_file_path = sink.getFile()

//     )
//   }

query predicate session_check(
  DataFlow::Node sink, string container_name,File session_file_path) {
    exists(|
      sink = wx_session().(DataFlow::Node)
      and
      container_name = sink.getContainer().(Function).getName()
      and
      container_name.matches(pageFunction())
      and
      session_file_path = sink.getFile()
    )
  
}