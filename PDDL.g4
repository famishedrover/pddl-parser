grammar PDDL;

//--------- DOMAIN ----------------

domain: LP DEFINE
  LP DOMAIN name=NAME RP
  ( requirements=requireDef
  | types=typesDef
  | constants=constantsDef
  | predicates=predicatesDef
  // functionsDef?
  )*
  operators+=structureDef*
  RP;

// Requirements
requireDef: LP REQUIREMENTS keys+=REQUIRE_KEY+ RP;

// Types
typesDef: LP TYPES types=typedList RP;
typedList: types+=NAME+ OF supertype=NAME typedList
  | types+=NAME*;
 /*typeDef:  LP EITHER either+=NAME+ RP
  | name=NAME;
*/

// Constants
constantsDef: LP CONSTANTS typedObjList RP;
typedObjList: names+=NAME+ OF objtype=NAME typedObjList
  | names+=NAME*;

// Predicates
predicatesDef: LP PREDICATES predicateDef+ RP;
predicateDef: LP predicate=nameDef typedVarList RP;
typedVarList: names+=VARIABLE+ OF vartype=NAME typedVarList
  | names+=VARIABLE*;

// Functions
// TODO

// Operators
structureDef: actionDef;
  //| durationActionDef;

// Action
actionDef: LP ACTION name=NAME
  (PARAMETERS LP parameters=typedVarList RP)?
  (PRECONDITION precondition=goalDef)?
  (EFFECT effect=effectDef)?
  (OBSERVE observe=observeDef)?
  RP;

goalDef
  : LP RP
  | atomicFormula
  | literal // :negative-precondition
  // :disjunctive-preconditions
  // :universal-preconditions
  // :existential-preconditions
  // :fluents
  | LP AND ands+=goalDef* RP
  ;

effectDef
  : LP RP
  | LP AND ands+=cEffect* RP
  | cEffect
  ;

cEffect
  : LP FORALL LP variables+=VARIABLE* RP effectDef RP
  | LP WHEN when=goalDef condEffect RP
  | literal
  ;

// pEffect
  // :fluents

condEffect
  : LP AND ands+=literal* RP
  | literal
  ;

observeDef: atomicFormula;

literal
  : atomicFormula
  | LP NOT atomicFormula RP;
atomicFormula: LP predicate=nameDef arguments+=term* RP;
term
  : name=NAME
  | variable=VARIABLE;

//--------- TOKENS ----------------
LP: '(';
RP: ')';
OF: '-';

DEFINE: 'define';
DOMAIN: 'domain';
REQUIREMENTS: ':requirements';
TYPES: ':types';
CONSTANTS: ':constants';
PREDICATES: ':predicates';

// Action Tokens
ACTION: ':action';
PARAMETERS: ':parameters';
PRECONDITION: ':precondition';
EFFECT: ':effect';
OBSERVE: ':observe';

// Others
NOT: 'not';
AND: 'and';
FORALL: 'forall';
WHEN: 'when';
EITHER: 'either';

REQUIRE_KEY:
 ':strips' // Basic STRIPS-style adds and deletes
 | ':typing' //	Allow type names in declarations of variables
 | ':negative-preconditions' //	Allow not in goal descriptions
 | ':disjunctive-preconditions' //	Allow or in goal descriptions
 | ':equality' //	Support = as built-in predicate
 | ':existential-preconditions' //	Allow exists in goal descriptions
 | ':universal-preconditions' //	Allow forall in goal descriptions
 | ':quantified-preconditions' //	= :existential-preconditions + :universal-preconditions
 | ':conditional-effects' // Allow when in action effects
 | ':fluents' //	Allow function definitions and use of effects using assignment operators and arithmetic preconditions.
 | ':adl' //	= :strips + :typing + :negative-preconditions	+ :disjunctive-preconditions + :equality	+ :quantified-preconditions	+ :conditional-effects
 | ':durative-actions' //	Allows durative actions. Note that this does not imply :fluents.
 | ':duration-inequalities' //	Allows duration constraints in durative actions using inequalities.
 | ':continuous-effects' //	Allows durative actions to affect fluents	continuously over the duration of the actions.
;

/*
 * allowing keywords as identifier where allowed
 * may need more to specify
 */
nameDef
	: NAME
//	| 'at'
//	| 'over'
	;

NAME: LETTER ANY_CHAR* ;
fragment LETTER:	'a'..'z' | 'A'..'Z';
fragment ANY_CHAR: LETTER | '0'..'9' | '-' | '_';

VARIABLE : '?' LETTER ANY_CHAR* ;

NUMBER : DIGIT+ ('.' DIGIT+)? ;
fragment DIGIT: '0'..'9';

LINE_COMMENT
    : ';' ~('\n'|'\r')* '\r'? '\n' -> skip
    ;
WHITESPACE
    :   (   ' '
        |   '\t'
        |   '\r'
        |   '\n'
        )+
        -> skip
    ;
