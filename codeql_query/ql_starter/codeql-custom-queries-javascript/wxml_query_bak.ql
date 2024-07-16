import javascript
import DataFlow


/**
 * @name wxml_query
 * @id wxml_query
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

 File get_file_loc(Location loc){
  result = loc.getFile()
 }


HTML::Attribute get_target_attribute(HTML::Element tmp)
{
  exists(
    HTML::Attribute target_attr| 
    target_attr.toString().matches("%shareIn%")
    and
    target_attr = tmp.getAnAttribute()
    |
  result = target_attr
  )
}

query predicate wxml_get_function(
  HTML::Element taget_element,HTML::Attribute target_attribute)
{
  exists( 
    HTML::Element tmp |
    //get_spec_loc(source.asExpr().getLocation())
    //target_attribute = tmp.getAnAttribute()
    target_attribute = get_target_attribute(tmp)

    and taget_element = tmp

  )
  //exists(WXML_TAINT wt| wt.hasFlow(source, sink))
  
  }


  query predicate wxml_get_function_loc(
    string target_element_loc,HTML::Attribute target_attribute,File raw_file_path)
  {
    exists( 
      HTML::Element tmp |
      //get_spec_loc(source.asExpr().getLocation())
      //target_attribute = tmp.getAnAttribute()
      target_attribute = get_target_attribute(tmp)
      and target_element_loc = get_spec_loc(tmp.getLocation())
      and raw_file_path = get_file_loc(tmp.getLocation())
  
    )
    //exists(WXML_TAINT wt| wt.hasFlow(source, sink))
    
    }