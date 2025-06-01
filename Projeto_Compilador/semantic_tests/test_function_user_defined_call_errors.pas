program CallErrors;
var 
  i: INTEGER;
  s: STRING;

FUNCTION MyTestFunc(val: INTEGER; flag: BOOLEAN): STRING;
  BEGIN
    IF flag THEN MyTestFunc := 'OK'
    ELSE MyTestFunc := 'NO';
  END;

BEGIN
  s := MyTestFunc(10, TRUE);          { Válido }
  WRITELN(s);
  
  s := MyTestFunc(10);                { Erro: número errado de args }
  i := MyTestFunc(5, FALSE);          { Erro: tipo de retorno STRING para INTEGER i }
  s := MyTestFunc('hello', TRUE);     { Erro: tipo de argumento 'hello' para INTEGER val }
END.