(declare-fun x1 () Int)
(declare-fun x2 () Int)
(declare-fun x3 () Int)

(declare-fun y1 () Bool)
(declare-fun y2 () Bool)
(declare-fun y3 () Bool)


; Una maquina virtual está exactamente en un servidor
(assert (and (<= x1 3) (> x1 0)))
(assert (and (<= x2 3) (> x2 0)))
(assert (and (<= x3 3) (> x3 0)))

; Un servidor está usado si tiene una máquina virtual creada en él.
;(assert (=> (or(= x1 1) (= x2 1) (= x3 1)) y1))
;(assert (=> (or(= x1 2) (= x2 2) (= x3 2)) y2))
;(assert (=> (or(= x1 3) (= x2 3) (= x3 3)) y2))


; si un servidor está usado es que hay una máquina virtual creada en él.
(assert (=> y1 (or(= x1 1) (= x2 1) (= x3 1))) )
(assert (=> y2 (or(= x1 2) (= x2 2) (= x3 2))) )
(assert (=> y3 (or(= x1 3) (= x2 3) (= x3 3))) )


; Constraints de capacidad 
;(assert (<= (+ (* 100 (ite (= x1 1) 1 0)) 
;               (* 50  (ite (= x2 1) 1 0)) 
;               (* 15  (ite (= x3 1) 1 0))) 
;            100 ))
(assert (<= (+ (* 100 (ite (= x1 1) 1 0)) 
               (* 50  (ite (= x2 1) 1 0)) 
               (* 15  (ite (= x3 1) 1 0))) 
            (* 100 (ite y1 1 0))))

(assert (<= (+ (* 100 (ite (= x1 2) 1 0)) 
               (* 50  (ite (= x2 2) 1 0)) 
               (* 15  (ite (= x3 2) 1 0)))  
            (* 75 (ite y2 1 0))))
            
(assert (<= (+ (* 100 (ite (= x1 3) 1 0)) 
               (* 50  (ite (= x2 3) 1 0)) 
               (* 15  (ite (= x3 3) 1 0))) 
            (* 200 (ite y3 1 0))))


; Objetivos de optimización

; minimizar uso servidores
(assert-soft (not y1) :id num_servers)
(assert-soft (not y2) :id num_servers)
(assert-soft (not y3) :id num_servers)

; minimizar coste diario
(assert-soft (not y1) :id costs :weight 10)
(assert-soft (not y2) :id costs :weight 5)
(assert-soft (not y3) :id costs :weight 20)


(check-sat)


;pedimos la solución
(get-value (x1) )
(get-value (x2) )
(get-value (x3) )

(get-value (y1) )
(get-value (y2) )
(get-value (y3) )

