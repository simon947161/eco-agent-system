import ast,hashlib,json,datetime
from pathlib import Path
sync=Path('qa/csoi-navigation-browser.py');asyn=Path('qa/csoi-navigation-async-browser.py');a=ast.parse(sync.read_text());b=ast.parse(asyn.read_text())
class RemoveAwait(ast.NodeTransformer):
 def visit_Await(self,n):return self.visit(n.value)
 def visit_AsyncFunctionDef(self,n):
  self.generic_visit(n);return ast.FunctionDef(name=n.name,args=n.args,body=n.body,decorator_list=n.decorator_list,returns=n.returns,type_comment=n.type_comment,type_params=[])
b=RemoveAwait().visit(b)
def equal(x,y):return ast.dump(x,include_attributes=False)==ast.dump(y,include_attributes=False)
checks={}
for name in ['ready','settled','result','research','tool']:
 checks[name]=equal(next(n for n in a.body if isinstance(n,ast.FunctionDef)and n.name==name),next(n for n in b.body if isinstance(n,ast.FunctionDef)and n.name==name))
original=next(n for n in a.body if isinstance(n,ast.Try)).body[0].body[1]
converted=next(n for n in b.body if isinstance(n,ast.FunctionDef)and n.name=='run_navigation').body[0]
# The only added loop operation attaches the service response adapter before goto.
removed=[n for n in converted.body if isinstance(n,ast.Expr)and isinstance(n.value,ast.Call)and isinstance(n.value.func,ast.Attribute)and n.value.func.attr=='route']
assert len(removed)==1
converted.body=[n for n in converted.body if n not in removed]
checks['fullViewportLoopExceptTransportBinding']=equal(original,converted)
assert all(checks.values()),checks
Path('qa/navigation-repair-20261102/async-assertion-equivalence.json').write_text(json.dumps({'at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'PASS','syncSha256':hashlib.sha256(sync.read_bytes()).hexdigest(),'asyncSha256':hashlib.sha256(asyn.read_bytes()).hexdigest(),'checks':checks,'scope':'AST identity after removing awaits and the single response-adapter binding. No assertions, timeouts, input cases or operation order removed.'},indent=2)+'\n')
print(checks)
