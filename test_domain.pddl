(define (domain Rover)
(:requirements :strips :typing)
(:types rover waypoint store camera mode lander objective)
(:constants  o1 o2 o3 - waypoint)

(:predicates (at ?x - rover ?y - waypoint)
             (can_traverse ?r - rover ?x - waypoint ?y - waypoint)
	     (calibrated ?c - camera ?r - rover ?w - waypoint ?o - objective)
             (available ?r - rover)
             (visible ?w - waypoint ?p - waypoint)
 	     (at_soil_sample ?w - waypoint)
	     (true)
)

(:action navigate
:parameters (?x - rover ?y - waypoint ?z - waypoint ?c - camera ?p - objective)
:precondition (and (can_traverse ?x ?y ?z) (available ?x) (at ?x ?y)
                (visible ?y ?z)
	    )
:effect (and (not (at ?x ?y))
  (at ?x ?z)
  (not (calibrated ?c ?x ?z ?p))
)
)


(:action sense_vis
 :parameters (?x - rover ?t - objective ?z - waypoint )
 :precondition (at ?x ?z)
 :observe (visible_from ?t ?z))


)
