[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/-Z5ovbbf)

Para resolver o problema de deadlock foram utilzados semáforos onde, caso o filósofo pegue o primeiro garfo e não consiga o pegar o segundo, ele libera o primeiro.

Para resolver o problema de starvation, cada filósofo verifica se o seus vizinhos não estão mais faminto do que ele (com um tempo maior desde que solicitou os garfos). Caso o vizinho esteja mais faminto, o filósofo em questão espera o outro pegar o garfo primeiro.
