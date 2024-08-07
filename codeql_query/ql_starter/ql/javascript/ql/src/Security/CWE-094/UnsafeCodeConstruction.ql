/**
 * @name Unsafe code constructed from library input
 * @description Using externally controlled strings to construct code may allow a malicious
 *              user to execute arbitrary code.
 * @kind path-problem
 * @problem.severity warning
 * @security-severity 6.1
 * @precision medium
 * @id js/unsafe-code-construction
 * @tags security
 *       external/cwe/cwe-094
 *       external/cwe/cwe-079
 *       external/cwe/cwe-116
 */

import javascript
import DataFlow::PathGraph
import semmle.javascript.security.dataflow.UnsafeCodeConstruction::UnsafeCodeConstruction

from Configuration cfg, DataFlow::PathNode source, DataFlow::PathNode sink
where cfg.hasFlowPath(source, sink)
select sink.getNode(), source, sink, "$@ flows to this location and is later $@.", source.getNode(),
  "Library input", sink.getNode().(Sink).getCodeSink(), "interpreted as code"
