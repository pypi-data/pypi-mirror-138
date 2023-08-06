PySeqTest ⚡️
================

O PySeqTest foi criado pensando em testes em sequência, executando os
testes um a um. Esse tipo de teste é útil quando testamos algo que
envolve arquivos, banco de dados, conexões a rede, etc. O objetivo do
``pyseqtest`` é ser simples, com verificações de valores boleanos,
comparações e exceções.

Exemplo de uso
--------------

Vamos começar a utilizar o PySeqTest! Neste primeiro exemplo, faremos o
teste de uma simples calculadora. Veja o código:

.. code:: python

   import pyseqtest


   class TestCalculator(pyseqtest.SeqTest):
       def __init__(self):
           super().__init__()

       def test_sum(self):
           condition = (10 + 5) == 15
           self.is_true(condition)

       def test_multiplication(self):
           condition = (2 * 5) == 4
           self.is_false(condition)

       def test_division(self):
           # error demonstration
           condition = (10 / 2) == 90
           self.is_true(condition, msg_error='Oh, the result is wrong')


   if __name__ == '__main__':
       TestCalculator().run()

No código acima, utilizamos os os seguintes métodos do ``pyseqtest``:

1. ``is_true``: Verifica se o valor é verdadeiro;
2. ``is_false``: Verifica se o valor é falso.

Em todos os métodos que verificam o resultado, podemos especificar,
opcionalmente, uma mensagem de erro caso o resultado não seja o
esperado.

Após executar o teste, o resultado será:

::

   PySeqTest
   =========
   3 testes presentes.

   0:00:00.000018: test_sum
   0:00:00.000009: test_multiplication
   ==============================
   [ ERROR ] test_division: Oh, the result is wrong

Todos os métodos para afirmação de teste
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. ``is_true``: Verifica se o valor é verdadeiro;
2. ``is_false``: Verifica se o valor é falso;
3. ``is_none``: Verifica se o valor None;
4. ``check_any_value``: Verifica se o valor de entrada e igual ao valor
   esperado.

Utilizando ``check_any_value``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

O ``check_any_value`` é utilizado para verificar dois valores: o valor
de entrada, e o valor de saída esperado. Veja um exemplo:

.. code:: python

   import pyseqtest


   class TestCalculator(pyseqtest.SeqTest):
       def __init__(self):
           super().__init__()

       def test_sum(self):
       # em vez de:
       condition = (10 + 5) == 10
       self.is_true(condition)

       # podemos fazer assim:
       self.check_any_value(15, 10)

       # o primeiro parâmetro é o valor
       # de entrada, o segundo, é valor
       # de saída esperado.

Neste exemplo, um erro seria retornado, já que 15 não é igual a 10.
