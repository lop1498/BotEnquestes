grammar Enquestes;

root: expr EOF;

expr: IDP ': PREGUNTA' PREGUNTA expr | IDR ': RESPOSTA' resposta expr | IDI ': ITEM' IDP '->' IDR expr | IDA ': ALTERNATIVA' alternativa expr | 'E: ENQUESTA' enquesta expr| 'END';

alternativa: IDI '['opcions']';
opcions: '(' NUM ',' IDI ')' ',' opcions | '(' NUM ',' IDI ')';

resposta: NUM ':' RESPOSTA resposta | NUM ':' RESPOSTA;

item: IDP '->' IDR;

enquesta: IDI enquesta | IDI;

PREGUNTA: (' '| [0-9a-zA-Z\u0080-\u00FF])+'?';
RESPOSTA: (' '| [0-9a-zA-Z\u0080-\u00FF])+';';

IDP: 'P'NUM;
IDR: 'R'NUM;
IDI: 'I'NUM;
IDA: 'A'NUM;
NUM: [0-9]+;

WS: [ \n]+ -> skip;

