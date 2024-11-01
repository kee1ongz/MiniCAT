import javascript
import DataFlow
//to make codeql get error.
//import DataFlow::PathGraph
/**
 * @name miniCSRF_all_in_one_baidu
 * @id mini_csrf_all_baidu
 * @kind problem
 * @problem.severity warning
 */


 string get_spec_loc(Location loc) {
    result = 
    loc.getFile() + "|" + // | cannot use in windows filename, it's a good choice to be the split sign.
    loc.getStartLine() + 
    ":" + loc.getStartColumn()+
    ":" + loc.getEndLine() +
     ":" + loc.getEndColumn()
   }
  


string selectRoute(){
    result = "%.redirectTo"
    or
    result = "%.reLaunch"
    or
    result = "%.navigateTo" 
}


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

private DataFlow::InvokeNode baidu_session() { result.getCalleeNode().toString().matches(sessionCheck()) }


private DataFlow::InvokeNode baidu_navi() { result.getCalleeNode().toString().matches(selectRoute()) }


class MiniCAT extends TaintTracking::Configuration {
  MiniCAT() { this = "meow" }

  override predicate isSource(DataFlow::Node source) { 
    exists(ObjectExpr pa| pa.flow().getALocalSource().(DataFlow::Node)=source )
    or
    exists(DotExpr pe| pe.flow().getALocalSource().(DataFlow::Node)=source)
    
  }

  override predicate isSink(DataFlow::Node sink) {

    baidu_navi().getOptionArgument(0, "url").(DataFlow::Node) = sink

  }

}


  string func_name(DataFlow::Node source)
  {
   if not source.getContainer().getScope().getOuterScope() instanceof FunctionScope
    and source.getContainer().inExternsFile()
    then result =  source.getContainer().(Expr).getAPredecessor().toString()
   else 
   result = 
   source.getContainer().(Expr).getAPredecessor()
   .getContainer().(Expr).getAPredecessor()
   .toString()
  }

  query predicate get_func(
    string sink_loc, 
    string source_loc,
    BasicBlock block_name,
    //ControlFlowNode source_func
    string source_func
    ){
    exists(
      MiniCAT pt,DataFlow::Node sink,DataFlow::Node source| 
      pt.hasFlow(source, sink)
    and source_loc= get_spec_loc(source.asExpr().getLocation())
    and sink_loc = get_spec_loc(sink.asExpr().getLocation())
    //and source_func = source.getContainer().(Expr).getAPredecessor()
    and source_func = source.getContainer().(Function).getName()
    and block_name = source.getBasicBlock()
    )
  }


// this is work for scope can be distinguished by module scope/toplevel scope/function scope etc.
//not work for all functionScope meme
  query predicate pure_get_func(
    string sink_loc,
    string source_loc,
    BasicBlock block_name,
    string source_func){
    exists(
      MiniCAT pt,DataFlow::Node sink,DataFlow::Node source|
      pt.hasFlow(source, sink)|
    source_loc= get_spec_loc(source.asExpr().getLocation())
    and sink_loc = get_spec_loc(sink.asExpr().getLocation())
    and source_func = func_name(source)
    and block_name = source.getBasicBlock()
    )
  }

  query predicate string_get_func(
    DataFlow::Node sink,DataFlow::Node source,
    Location block_name,
    //ControlFlowNode source_func
    string source_func
    ){
    exists(
      MiniCAT pt| 
      pt.hasFlow(source, sink)|
      source_func = source.getContainer().(Function).getName()
    and block_name = source.getBasicBlock().getLocation()
    )
  }

//only for debug
/*query predicate pure_get_func_raw(
  DataFlow::Node sink,DataFlow::Node source,
  string block_name,
  string source_func){
  exists(
    MiniCAT pt|
    pt.hasFlow(source, sink)|
  source_func = func_name(source)
  and block_name = source.getBasicBlock()
  )
}*/

query predicate get_func_raw(
  DataFlow::Node sink,DataFlow::Node source,
  string block_name,
  ControlFlowNode source_func){
  exists(
    MiniCAT pt| 
    pt.hasFlow(source, sink)|
  source_func = source.getContainer().(Expr).getAPredecessor()
  //and source_func = source.getContainer().(Function).getName()
  and block_name = source.getBasicBlock().toString()
  )
}


query predicate session_check(
    DataFlow::Node sink, string container_name,File session_file_path) {
      exists(|
        sink = baidu_session().(DataFlow::Node)
        and
        container_name = sink.getContainer().(Function).getName()
        and
        container_name.matches(pageFunction())
        and
        session_file_path = sink.getFile()
      )
    
  }

// //debug park
// class CanUwriteAdoc extends TaintTracking::Configuration {
//   CanUwriteAdoc() { this = "Best way to learn CodeQL:brute force learning" }

//   override predicate isSource(DataFlow::Node source) { 
//     any()
    
//   }

//   override predicate isSink(DataFlow::Node sink) {

//     wx_navi().getOptionArgument(0, "url").(DataFlow::Node) = sink

//   }

// }


// query predicate debug_pure_get_func_raw(
//   DataFlow::Node sink,DataFlow::Node source,
//   string block_name,
//   string source_func){
//   exists(
//     CanUwriteAdoc pt|
//     pt.hasFlow(source, sink)|
//   source_func = func_name(source)
//   and block_name = source.getBasicBlock().toString() 
//   )
// }

// query predicate debug_get_func_raw(
//   DataFlow::Node sink,DataFlow::Node source,
//   string block_name,
//   ControlFlowNode source_func){
//   exists(
//     CanUwriteAdoc pt| 
//     pt.hasFlow(source, sink)|
//   source_func = source.getContainer().(Expr).getAPredecessor()
//   //and source_func = source.getContainer().(Function).getName()
//   and block_name = source.getBasicBlock().toString()
//   )
// }


/*
class WXML_TAINT extends TaintTracking::Configuration {
  WXML_TAINT() { this = "wow" }

  override predicate isSource(DataFlow::Node source) { 
   any()
    
  }

  override predicate isSink(DataFlow::Node sink) {

   exists( HTML::Element tmp,string name| tmp.getAttributeByName(name)|
   
   sink = tmp.

   
   )

  }

}*/