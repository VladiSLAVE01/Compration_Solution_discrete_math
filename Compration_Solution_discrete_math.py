def extended_gcd(a, b):
	"""Расширенный алгоритм Евклида. Возвращает (gcd, x, y): a*x + b*y = gcd"""
	if b == 0:
		return (a, 1, 0)
	else:
		g, x1, y1 = extended_gcd(b, a % b)
		return (g, y1, x1 - (a // b) * y1)


def gcd(a, b):
	"""НОД через расширенный алгоритм Евклида"""
	return extended_gcd(a, b)[0]


def solve_comparison(a, b, m):
	"""
	Решает линейное сравнение a*x ≡ b (mod m)
	Возвращает список всех решений по модулю m
	"""
	print(f"Решаем сравнение: {a}·x ≡ {b} (mod {m})")
	print("-" * 60)

	# Шаг 1: Находим НОД(a, m)
	d = gcd(a, m)
	print(f"1. НОД({a}, {m}) = {d}")

	# Шаг 2: Проверяем, делится ли b на НОД
	if b % d != 0:
		print(f"2. {b} не делится на {d} → решений нет")
		return []

	print(f"2. {b} делится на {d} → решений будет {d} штук")

	# Шаг 3: Сокращаем сравнение
	a1, b1, m1 = a // d, b // d, m // d
	print(f"3. Сокращаем на {d}: {a1}·x ≡ {b1} (mod {m1})")

	# Шаг 4: Находим обратный элемент к a1 по модулю m1
	# Для этого решаем a1·x ≡ 1 (mod m1) через расширенный алгоритм Евклида
	g, inv, _ = extended_gcd(a1, m1)
	# inv - это x, такой что a1*x ≡ 1 (mod m1)

	# Шаг 5: Находим частное решение
	x0 = (inv * b1) % m1
	print(f"4. Частное решение в сокращённой системе: x₀ = {x0} (mod {m1})")

	# Шаг 6: Находим все решения в исходной системе
	solutions = []
	for k in range(d):
		sol = (x0 + k * m1) % m
		solutions.append(sol)

	print(f"\n5. Все {d} решений исходного сравнения:")
	solutions_sorted = sorted(solutions)
	for i, sol in enumerate(solutions_sorted):
		print(f"   x ≡ {sol} (mod {m})")

	return solutions


def solve_with_euclidean_algorithm(a, b, m, show_steps=True):
	"""
	Решает сравнение через алгоритм Евклида с подробными шагами
	(альтернативный метод с цепными дробями)
	"""
	print(f"\n" + "=" * 60)
	print(f"МЕТОД АЛГОРИТМА ЕВКЛИДА (с цепными дробями)")
	print(f"Решаем: {a}·x ≡ {b} (mod {m})")
	print("=" * 60)

	# Шаг 1: НОД
	d = gcd(a, m)
	print(f"\nШаг 1: Вычисляем НОД({a}, {m})")

	# Записываем шаги алгоритма Евклида
	remainder_steps = []
	temp_a, temp_m = a, m

	while temp_m != 0:
		q = temp_a // temp_m
		r = temp_a % temp_m
		remainder_steps.append((temp_a, temp_m, q, r))
		temp_a, temp_m = temp_m, r

	if show_steps:
		print("   Алгоритм Евклида:")
		for step in remainder_steps:
			print(f"   {step[0]} = {step[2]}·{step[1]} + {step[3]}")

	print(f"   НОД = {d}")

	# Проверка существования решений
	if b % d != 0:
		print(f"\n{b} не делится на {d} → решений нет")
		return []

	print(f"\nШаг 2: {b} делится на {d} → решений будет {d}")

	# Сокращаем
	a1, b1, m1 = a // d, b // d, m // d
	print(f"\nШаг 3: Сокращаем на {d}: {a1}·x ≡ {b1} (mod {m1})")

	# Находим неполные частные для a1 и m1
	q_list = []
	temp_a, temp_m = a1, m1
	while temp_m != 0:
		q = temp_a // temp_m
		r = temp_a % temp_m
		q_list.append(q)
		temp_a, temp_m = temp_m, r

	print(f"\nШаг 4: Неполные частные: {q_list}")

	# Вычисляем Pn (числители подходящих дробей)
	P = [1, q_list[0]]  # P0 = 1, P1 = q0
	for i in range(2, len(q_list)):
		P.append(q_list[i] * P[i - 1] + P[i - 2])

	print(f"   Pk: {P}")

	# n - количество неполных частных (до остатка 1)
	n = len(q_list)
	Pn_1 = P[-2] if len(P) >= 2 else 1  # P_{n-1}

	print(f"\nШаг 5: n = {n}, P_{n - 1} = {Pn_1}")

	# Частное решение по формуле x0 = (-1)^(n-1) * Pn_1 * b1 (mod m1)
	sign = (-1) ** (n - 1)
	x0 = (sign * Pn_1 * b1) % m1

	print(f"   x₀ = (-1)^{n - 1}·P_{n - 1}·b₁ = {sign}·{Pn_1}·{b1} = {x0} (mod {m1})")

	# Все решения
	solutions = []
	for k in range(d):
		sol = (x0 + k * m1) % m
		solutions.append(sol)

	print(f"\nШаг 6: Все {d} решений исходного сравнения:")
	for i, sol in enumerate(sorted(solutions)):
		print(f"   x ≡ {sol} (mod {m})")

	return solutions


def main():
	print("=" * 60)
	print("РЕШЕНИЕ ЛИНЕЙНОГО СРАВНЕНИЯ")
	print("=" * 60)

	# Ввод данных
	print("\nВведите параметры сравнения a·x ≡ b (mod m)")

	# Для конкретного примера:
	a = 14546
	m = 19929
	alpha = 6  # число рождения
	b = 7 * alpha

	print(f"\nИсходные данные:")
	print(f"  a = {a}")
	print(f"  m = {m}")
	print(f"  α = {alpha} (число рождения)")
	print(f"  b = 7·α = {b}")
	print(f"\nСравнение: {a}·x ≡ {b} (mod {m})\n")

	# Метод 1: Простой
	print("\n" + "=" * 60)
	print("МЕТОД 1: СТАНДАРТНЫЙ АЛГОРИТМ")
	print("=" * 60)
	solutions1 = solve_comparison(a, b, m)

	# Метод 2: С алгоритмом Евклида и цепными дробями
	solutions2 = solve_with_euclidean_algorithm(a, b, m, show_steps=True)

	# Проверка решений
	print("\n" + "=" * 60)
	print("ПРОВЕРКА РЕШЕНИЙ")
	print("=" * 60)
	if solutions1:
		d = gcd(a, m)
		print(f"\nПроверяем каждое решение (должно быть: a·x mod m = {b}):")
		for sol in sorted(solutions1):
			result = (a * sol) % m
			status = "✓" if result == b else "✗"
			print(f"  {status} {a}·{sol} mod {m} = {result} (должно быть {b})")

	print("\n" + "=" * 60)
	print("ГОТОВО!")
	print("=" * 60)


if __name__ == "__main__":
	main()
