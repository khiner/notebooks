### A Pluto.jl notebook ###
# v0.19.19

using Markdown
using InteractiveUtils

# ╔═╡ d3525d21-d733-4b66-84ad-13fa437dd8bf
using LaTeXStrings, Plots, StaticArrays

# ╔═╡ c39fc80a-44a8-42d8-911c-bf1c937e6bba
struct V2
	value::SVector{2,Number} # Arrow extends to this point (minus `origin`).
	origin::SVector{2,Number} # Arrow starts at this point.
	plottype::Symbol # Plot as either a line or point (defaults to :line).
	arrow::Symbol # Arrow type: (:arrow, :closed, :open, :none)
	label::Union{String,Nothing} # Label shown in the legent.
	annotation::Union{String,Nothing} # Label shown in the chart, half way along.
	annotationpos::Symbol # Annotation position: (:middle = middle of vector, :end = end of vector. :middle only allowed when plottype == :line.)
	annotationanchor::Symbol # Annotation anchor: (:left, :center, :right)
	annotationoffset::SVector{2,Float64}
	annotationsize::Int64 # Annotation font size.
	linewidth::Float64 # Line width.
	linestyle::Symbol # Line style: (:auto, :solid, :dash, :dot, :dashdot, :dashdotdot)
	color::Union{Symbol,Int64} # Line color.

    function V2(value;
		o=[0.,0.], pt=:line, arrow=:arrow, l=nothing,
		a=nothing, ap=:end, aa=:left,
		ao=(ap==:middle ? [0.15,0.15] : aa == :left ? [0.15, 0.] : [0.,0.]), asz=14,
		lw=1., ls=:solid, c=:auto)
		new(value, o, pt, arrow, l, a, ap, aa, ao, asz, lw, ls, c)
	end
end

# ╔═╡ e9539e47-dc78-43e7-81de-f3e3267ed197
function Plots.plot(vectors::Vararg{V2}; kw...)
	plt = plot([]; label="", aspect_ratio=:equal, kw...)
	for v in vectors
		o = v.origin
		val = o + v.value
		if v.plottype == :line
			plot!(
				[o.x, val.x], [o.y, val.y];
				linewidth=v.linewidth, linestyle=v.linestyle, arrow=v.arrow, label=v.label, c=v.color
			)
		else
			scatter!([val.x], [val.y]; label=v.label, c=v.color)
		end
		if v.annotation != nothing
			ap = v.annotationpos
			ao = v.annotationoffset
			annotate!(
				(o + ao + (v.value * (ap == :middle ? 0.5 : 1)))..., text(v.annotation, v.annotationsize, v.annotationanchor)
			)
		end
	end

	return plt
end

# ╔═╡ b8245233-055a-43b6-8170-70eeccf83495
L"""
\newcommand{\s}{\enspace}
\newcommand{\R}{\mathbb{R}}
\newcommand{\b}[1]{\boldsymbol{#1}}
\newcommand{\v}[1]{\begin{bmatrix}#1\end{bmatrix}}
\newcommand{\m}[1]{\begin{bmatrix}#1\end{bmatrix}}
\newcommand{\align}[1]{\begin{align}#1\end{align}}
"""

# ╔═╡ 71c1f166-c912-4fea-8d56-84acdc46c083
# Hack: Since all md cells depend on the above cell defining LaTeX commands, re-run every cell below this one.
# From: https://discourse.julialang.org/t/how-to-force-a-pluto-recalculation/80532/6
html"""
<script>
	// Get current cell handle and ID
	let cell = currentScript.closest('pluto-cell')
	let id = cell.getAttribute('id')
	// Find all cells below the current one and extract their ids
	let cells_below = document.querySelectorAll(`pluto-cell[id='${id}'] ~ pluto-cell`)
	let cells_below_ids = [...cells_below].map((el) => el.getAttribute('id'))
	// Use the pluto internal function to re-run all selected cells
	cell._internal_pluto_actions.set_and_run_multiple(cells_below_ids)
	</script>
"""

# ╔═╡ 0fe32c74-93b0-11ed-0985-1dfb7d1bb10e
md"""
**1.** Describe geometrically (line, plane, or all of $\R^3$) all linear combinations of:

a) $\v{1\\2\\3}$ and $\v{3\\6\\9}$

Since $\v{3\\6\\9} = 3\v{1\\2\\3}$, the linear combination of both vectors is just $\s c\v{1\\2\\3}, c \in{\R}$.

This is the line crossing through the origin, $\begin{bmatrix}0\\0\\0\end{bmatrix}$, and $\begin{bmatrix}1\\2\\3\end{bmatrix}$.

b) $\v{1\\0\\0}$ and $\v{0\\2\\3}$

$c\v{1\\0\\0} + d\v{0\\2\\3} = \v{c\\2d\\3d}$

Keeping $c = 0$ and varying $d$ creates a line through the origin and $\v{0\\2\\3}$.
Varying $c$ extends the line across the $x$-dimension to form a plane with slope $\frac{2}{3}$ with respect to the $x$-axis.

c) $\v{2\\0\\0}$ and $\v{0\\2\\2}$ and $\v{2\\2\\3}$

Since none of these vectors can be expressed as a linear combination of the others, they span all of $\R^3$.
"""

# ╔═╡ 56dad226-65bc-4f0b-ab1f-c39c9e7b1270
md"""
**2.** Draw $\b{v} = \v{4\\1}$ and $\b{w} = \v{-2\\2}$ and $\b{v} + \b{w}$ and $\b{v} - \b{w}$ in a single $xy$ plane.
"""

# ╔═╡ b78fb4bf-c0f2-45b3-88bf-f3eb22094823
let
	v = [4, 1]; w = [-2, 2]
	plot(
		V2(v, lw=2, a=L"v", ap=:middle, ao=[0, 0.25], c=1),
		V2(w, lw=2, a=L"w", ap=:middle, c=2),
		V2(v+w, lw=4, a=L"v+w", ap=:middle, aa=:right, ao=[0, 0.4]),
		V2(v-w, lw=4, a=L"v-w", ap=:middle),
		V2(w, o=v, a=L"+w", ap=:middle, ls=:dash, c=2),
		V2(-w, o=v, a=L"-w", ap=:middle, ls=:dash, c=2),
	)
end

# ╔═╡ f1d4ce39-9e80-4042-b6a7-715260da57dc
md"""
**3.** If $\b{v} + \b{w} = \v{5\\1}$ and $\b{v} - \b{w} = \v{1\\5}$, compute and draw the vectors $\b{v}$ and $\b{w}$.

We have the system of equations:

$\align{
\b{v}_1 + \b{w}_1 &= 5\\
\b{v}_2 + \b{w}_2 &= 1\\
\b{v}_1 - \b{w}_1 &= 1\\
\b{v}_2 - \b{w}_2 &= 5\\
}$

Substitute $\b{w}$ variables and solve:

$\align{
\b{w}_1 &= \b{v}_1 - 1\\
\b{w}_2 &= \b{v}_2 - 5\\
}$

$\align{
\b{v}_1 + \b{w}_1 = 5 \implies \b{v}_1 + (\b{v}_1 - 1) = 5 \implies \b{v}_1 &= 3\\
\b{v}_2 + \b{w}_2 = 1 \implies \b{v}_2 + (\b{v}_2 - 5) = 1 \implies \b{v}_2 &= 3\\
\b{w}_1 &= \b{v}_1 - 1 \implies 3 - 1 = 2\\
\b{w}_2 &= \b{v}_2 - 5 \implies 3 - 5 = -2\\
}$

So, $\b{v} = \v{3\\3}$, and $\b{w} = \v{2\\-2}$.
"""

# ╔═╡ 696e90b5-a8c2-4803-9e74-2d29fef911df
let
	v = [3, 3]; w = [2, -2]
	plot(
		V2(v, lw=2, l=L"v", c=1),
		V2(w, lw=2, l=L"w", c=2),
		V2(v+w, lw=4, a=L"v+w", ap=:middle, ao=[0, -0.4]),
		V2(v-w, lw=4, a=L"v-w", ap=:middle, aa=:right, ao=[-0.3, 0]),
		V2(w, o=v, a=L"+w", ap=:middle, ls=:dash, c=2),
		V2(-w, o=v, a=L"-w", ap=:middle, ls=:dash, c=2),
	)
end

# ╔═╡ b55d0ef6-f90d-475a-8097-a71e15064fb7
md"""
**4.** From $\b{v} = \v{2\\1}$ and $\b{w} = \v{1\\2}$, find the components of $3\b{v} + \b{w}$ and $c\b{v} + d\b{w}$.

$3\b{v} + \b{w} = \v{3 \cdot 2 + 1\\3 \cdot 1 + 2} = \v{7\\5}$
$c\b{v} + d\b{w} = \v{2c + d\\c + 2d}$
"""

# ╔═╡ 9640b2b8-0d72-458d-9511-b6b419ea80e5
md"""
**5.** Compute $\b{u}+\b{v}+\b{w}$ and $2\b{u}+2\b{v}+\b{w}$.

$\b{u} = \v{1\\2\\3}, \b{v} = \v{-3\\1\\-2}, \b{w} = \v{2\\-3\\-1}.$

$\b{u}+\b{v}+\b{w} = \v{1+(-3)+2\\2+1+(-3)\\3+(-2)+(-1)} = \v{0\\0\\0}$

$2\b{u}+2\b{v}+\b{w} = \v{2 \cdot 1+2 \cdot (-3)+2\\2 \cdot 2+2 \cdot 1+(-3)\\2 \cdot 3+2 \cdot (-2)+(-1)} = \v{-2\\3\\1}$

How do you know $\b{u}, \b{v}, \b{w}$ lie in a plane?

**These lie in a plane because $\b{w} = c\b{u} + d\b{v}$.
Find $c$ and $d$.**

We only need a system of two equations to find the two variables $c$ and $d$.
We can use substitution with two of the components:

$\align{
\b{w}_1 &= c\b{u}_1 + d\b{v}_1\\
\b{w}_2 &= c\b{u}_2 + d\b{v}_2\\
\implies\\
2 &= c - 3d\\
-3 &= 2c + d\\
}$

Substituting $c = 3d + 2$:

$\align{
-3 &= 2c + d\\
-3 &= 2(3d + 2) + d\\
-7 &= 7d\\
d &= -1, \text{and}\\
c &= 3d + 2 = -3 + 2 = -1
}$

Verifying:

$\align{
\b{w} &= c\b{u} + d\b{v}\\
&= (-1)\b{u} + (-1)d\b{v}\\

\v{2\\-3\\-1} &= -\v{1\\2\\3} - \v{-3\\1\\-2}\\
&= \v{-1+3\\-2-1\\-3+2}
}$
"""

# ╔═╡ b82d0e9b-4615-4107-b719-ff562893f893
md"""
**6.** Every combination of $\b{v} = (1,-2,1)$ and $\b{w} = (0,1,-1)$ has components that add to ____.
Find $c$ and $d$ so that $c\b{v} + d\b{w} = (3,3,-6)$.

$c$ must be equal to $3$, since $\b{w}_1 = 0$. Using the second components to find $d$:

$\align{
c\b{v}_2 + d\b{w}_2 &= 3\\
3 \cdot (-2) + d \cdot 1 &= 3\\
-6 + d &= 3\\
d &= 9
}$

Verifying with $c = 3$ and $d = 9$:

$\align{
c\b{v} + d\b{w} &= \v{3\\3\\-6}\\
3\v{1\\-2\\1} + 9\v{0\\1\\-1} &= \v{3\\3\\-6}\\
\v{3+0\\-6+9\\3-9} &= \v{3\\3\\-6}
}$

**Why is $(3,3,6)$ impossible?**

There can be no $c$ and $d$ such that

$c\v{1\\-2\\1} + d\v{0\\1\\-1} = \v{3\\3\\6},$

since $c$ must be equal to $3$, and there is no $d$ that satisfies both the second and third components:

$\align{
3 \cdot (-2) + d &= 3 \implies d = 9\\
3 \cdot 1 - d &= 6 \implies d = -3
}$
"""

# ╔═╡ 1ccb54d8-0219-48d9-a282-303f67e646eb
md"""
**7.** In the $xy$ plane, mark all nine of these linear combinations:

$c\v{2\\1} + d\v{0\\1} \s \text{with} \s c = 0,1,2 \s \text{and} \s d = 0,1,2.$
"""

# ╔═╡ 70fdd975-62bc-4825-a872-d32b2f924362
let
	CD = []
	for c in (0,1,2)
		for d in (0,1,2)
			push!(CD, [c,d])
		end
	end
	plot(map(
		cd -> V2(cd[1]*[2,1] + cd[2]*[0, 1];
		pt=:point, a=L"c=%$(cd[1]), d=%$(cd[2])", c=1, asz=12), CD
	)...)
end

# ╔═╡ 0a1a8900-0da3-4c2c-849b-b5ebc6d979e2
md"""
**8.** The parallelogram in Figure 1.1 has diagonal $\b{v} + \b{w}.$
What is its other diagonal?
What is the sum of the two diagonals?
Draw that vector sum.

$\b{v} = \v{4\\2}, \b{w} = \v{-1\\2}$

Reproducing Fig. 1.1, and adding the other diagonal, $\b{v} - \b{w} = \v{5\\0},$ and the sum of the two diagonals, $\b{v} + \b{w} + (\b{v} - \b{w}) = 2\b{v}$:
"""

# ╔═╡ d804f088-e382-4e5d-ae5e-d256142e668e
let
	v = [4, 2]; w = [-1, 2]
	plot(
		V2(2v, a=L"2v", ap=:middle, ao=[0, -0.25], lw=4),
		V2(v, lw=2, l=L"v", c=1),
		V2(w, lw=2, l=L"w", c=2),
		V2(v+w, lw=2, a=L"v+w", ap=:middle, ao=[0.75, 0.75]),
		V2(v, o=w, c=1, a=L"+v", ap=:middle, aa=:right, ao=[0, 0.25], ls=:dash),
		V2(w, o=v, c=2, a=L"+w", ap=:middle, ls=:dash),
		V2(v-w, o=w, c=3, a=L"v-w", ap=:middle, aa=:right, ao=[-0.5, 0.25], ls=:dash),
		V2(v-w, o=v+w, c=3, a=L"+(v-w)", ap=:middle, aa=:center, ao=[0, 0.25], ls=:dash),
	)
end

# ╔═╡ 50d0dd29-e890-4144-8427-bceedd404642
md"""
**9.** If three corners of a parallelogram are $(1,1), (4,2),$ and $(1,3),$ what are all three of the possible fourth corners?
Draw two of them.

$\b{c1} = \v{1\\1}, \b{c2} = \v{1\\3}, \b{c3} = \v{4\\2}, \b{c4} = \v{?\\?}$

Let's plot the three given corners:
"""

# ╔═╡ 857ca64f-34cd-461f-8148-b56816232929
three_corners = [1;1;;1;3;;4;2] # each column is a corner

# ╔═╡ 9bbff24a-623a-403d-85df-109bfebd6c3b
plot(map(corner -> V2(corner[2]; a=L"c%$(corner[1])", pt=:point, c=1),
	enumerate(eachcol(three_corners)))...; xlims=(-3,5), ylims=(-1,5))

# ╔═╡ c36df7f9-e76a-45d6-aecc-f2c3d2e69ffa
md"""
Each pair of opposite sides of a parallelogram must have the same length.

We can visually see that the possible fourth corner $\b{c4}$ can be any of:

$\b{c4} \in \{\b{c3} + (\b{c2} - \b{c1}), \b{c3} - (\b{c2} - \b{c1}), \b{c2} - (\b{c3} - \b{c1})\}$

Let's see these solutions plotted out along with the other corners:
"""

# ╔═╡ 38f6fa60-4ce3-4107-9777-ab93d8a104f0
let
	c1, c2, c3 = eachcol(three_corners)
	possible_fourth_corners = (c3 + (c2-c1), c3 - (c2-c1), c2 - (c3-c1))
	pgram_corners = map(
		fourth_corner -> hcat(three_corners, fourth_corner),
		possible_fourth_corners
	)

	plots = map(
		corners -> plot(
			map(corner -> V2(corner[2]; a=L"c%$(corner[1])", pt=:point, ao=[0.4, 0.1], asz=12, c=1),
				enumerate(eachcol(corners)))...; xlims=(-3,5), ylims=(-1,5)
		), pgram_corners
	)
	plot(plots..., layout=3, aspect_ratio=:equal)
end

# ╔═╡ df1c4083-065b-4bca-a9a0-f70ed6bf4b52
md"""
**10.** Which point of the cube is $\b{i} + \b{j}$? Which point is the vector sum of $\b{i} = (1,0,0)$ and $\b{j} = (0,1,0)$ and $\b{k} = (0,0,1)$?
Describe all points $(x,y,z)$ in the cube.

$\align{
\mathbb{o} &\equiv (0,0,0)\\
\b{i} &= (1,0,0)\\
\b{j} &= (0,1,0)\\
\b{k} &= (0,0,1)\\
\b{i} + \b{j} &= (1,1,0)\\
\b{i} + \b{k} &= (1,0,1)\\
\b{j} + \b{k} &= (0,1,1)\\
\b{i} + \b{j} + \b{k} &= (1,1,1)
}$
"""

# ╔═╡ 50b358af-6c15-4a2c-a384-8ef0281b5469
md"""
**11.** Four corners of this unit cube are $(0,0,0),(1,0,0),(0,1,0),(0,0,1).$
What are the other four corners?

(All 8 corners are described above).

Find the coordinates of the center point of the cube.

$\text{center} = 0.5*(\b{i} + \b{j} + \b{k}) = (0.5, 0.5, 0.5).$

The center points of the six faces are:

$\align{
0.5(\b{i} + \b{j}) &= (0.5, 0.5, 0)\\
0.5(\b{i} + \b{k}) &= (0.5, 0, 0.5)\\
0.5(\b{j} + \b{k}) &= (0, 0.5, 0.5)\\
\b{k} + 0.5(\b{i} + \b{j}) &= (0.5, 0.5, 1)\\
\b{j} + 0.5(\b{i} + \b{k}) &= (0.5, 1, 0.5)\\
\b{i} + 0.5(\b{j} + \b{k})  &= (1, 0.5, 0.5)\\
}$

The cube has how many edges?

The cube has 12 edges (4 corners with 3 unique edges each).
"""

# ╔═╡ b6f029a0-8e39-4108-916a-5033b2ade7a2
md"""
**12.** _Review Question._
In $xyz$ space, where is the plane of all linear combinations of $i = (1,0,0)$ and $i + j = (1,1,0)$?

This is the plane along the "bottom" of the cube, perpendicular to the $k$-axis, composed of all points with $k = 0$.
"""

# ╔═╡ 84a67551-9ed1-42be-be5b-cc92acceffe8
md"""
**13.**

a) What is the sum $\b{V}$ of the twelve vectors that go from the center of a clock to the hourse 1:00, 2:00, ..., 12:00?

Since each vector has exactly one vector with the same magnitude going in the opposite direction, the sum of all vectors must be equal to the zero-vector $(0, 0)$.

b) If the 2:00 vector is removed, why do the 11 remaining vectors add to 8:00?

Using the same argument as for (a) above, all vectors have an opposite vector exactly cancelling it out.
If we remove any one of the vectors, the opposite vector will have nothing to cancel it out, while all remaining vectors still cancel.
Thus, since 8:00 corresponds to the vector opposite 2:00, it will be the only contribution to the sum that is not cancelled out.

c) What are the $x, y$ components of that 2:00 vector $\b{v} = (\cos{\theta},\sin{\theta})$?

Since $\b{v} = (\cos{\theta},\sin{\theta})$ is given, we know that the radius of the clock is $1$ unit.
2:00 is $\frac{1}{12}$ of the way, counter-clockwise, around the circle starting at 3:00 (where $\theta = 0$).
Thus, $\theta = \frac{1}{12}(2\pi) = \frac{\pi}{6}$, and we have:

$\b{v} = (\cos{\frac{\pi}{6}},\sin{\frac{\pi}{6}}) = (\frac{\sqrt{3}}{2}, \frac{1}{2}).$
"""

# ╔═╡ f44b3e22-6f72-41c0-8c26-1db04f32155d
md"""
**14.** Suppose the twelve vectors start from 6:00 at the bottom instead of $(0,0)$ at the center. The vector to 12:00 is doubled to $0,2)$. The new twelve vectors add to ____.

We are effectively moving the origin down by $1$.
This is equivalent to adding $(0, 1)$ to each vector.
Thus, the resulting sum will be $(0, 12)$.

To verify this result visually & empirically, let's first draw the original clock:
"""

# ╔═╡ 01533808-dad6-4afc-88ae-03bd5402009f
begin
	# Define an array Θ of angles indexable by the o'clock position,
	# s.t. Θ[3] == 0
	Θ_clock = circshift(0:11 |> reverse, 3) * pi/6
	@assert(Θ_clock[3] == 0)
	V_clock = [cos.(Θ_clock) sin.(Θ_clock)] # Each row of this matrix is an hour position on the unit clock.
end

# ╔═╡ 62cea919-4d7a-4432-b823-dfe16284fcf6
let
	Vectors_clock = map(iv -> V2(last(iv); a="$(first(iv))", aa=:center, ao=last(iv) * 0.15, l="", c=:black), eachrow(V_clock) |> enumerate)
	plot(Vectors_clock...; xlims=(-1.5, 1.5), ylims=(-1.5, 1.5))
end

# ╔═╡ 8dafef43-fc69-46c2-8ec0-48c7b839dfcf
md"Reproduce our $(0, 0)$ sum:"

# ╔═╡ bdc113bd-9e7f-44e9-b140-61a8f1727b0b
sum(V_clock; dims=1)

# ╔═╡ 34ddf40b-aa55-4441-913e-18956c2b1e93
md"Now, with the origin at 6:00..."

# ╔═╡ 46a4d33b-2ca1-476b-85bf-9f6c4c3a62b7
let
	V_clock_6_origin = V_clock .+ [0 1]
	Vectors_clock = map(iv -> V2(last(iv); a="$(first(iv) == 6 ? "" : first(iv))", aa=:center, ao=last(iv) * 0.1, l="", c=:black, o=[0,-1]), eachrow(V_clock_6_origin) |> enumerate)
	plot(Vectors_clock...; xlims=(-1.5, 1.5), ylims=(-1.5, 1.5))
end

# ╔═╡ 163f44c4-546f-4a29-a028-52d9b4f6be81
sum(V_clock .+ [0 1]; dims=1)

# ╔═╡ 4bd91592-20a9-4b34-a477-f5143a5e440d
md"""
Probs. **15-19** deal with the following $\b{v}$ and $\b{w}$: (The book does not define the vectors precisely, as the lessons work with arbitrary vectors.)
"""

# ╔═╡ 9ec03fac-1a30-4093-b480-e5b32e35ab5e
let
	w = [1, 6]; v = [6, 1]
	plot(
		V2(v, a=L"v", aa=:center),
		V2(w, a=L"w", aa=:center),
		V2(v - w; o=w, arrow=:none, ls=:dash),
		V2(0.5(v + w); a=L"u = \frac{1}{2}(v + w)", pt=:point);
		xlims=(0, 7)
	)
end

# ╔═╡ 2321a3e5-2f23-4478-812e-2f6e2ba28524
md"""
**15.** Mark the points $\frac{3}{4}\b{v} + \frac{1}{4}\b{w}$ and $\frac{1}{4}\b{v} + \frac{1}{4}\b{w}$ and $\b{v} + \b{w}$.
"""

# ╔═╡ 1f4804ba-fee7-4322-857a-eda7edbd7293
let
	v = [6, 1]; w = [1, 6]
	plot(
		V2(v, a=L"v"),
		V2(w, a=L"w"),
		V2(v - w; o=w, arrow=:none, ls=:dash),
		V2(0.75v + 0.25w; a=L"u = \frac{3}{4}v +\frac{1}{4}w", pt=:point, asz=12),
		V2(0.25v + 0.25w; a=L"u = \frac{1}{4}v + \frac{1}{4}w", pt=:point, asz=12),
		V2(v + w; a=L"u = v + w", pt=:point),
	)
end

# ╔═╡ 983448de-2e7f-46f0-92bc-d1cb30310a73
md"""
**16.** Mark the point $-\b{v} + 2\b{w}$ and any other combination $c\b{v} + d\b{w}$ with $c + d = 1$. Draw the line of all combinations that have $c + d = 1$.
"""

# ╔═╡ 3e607e6f-2b4f-486c-a09b-ae44616e5310
let
	v = [6, 1]; w = [1, 6]
	C = -1:0.25:2
	D = 1 .- C
	plot(
		V2(v, l=L"v"),
		V2(w, l=L"w"),
		V2(-3v+3w; o=2v-w, l=L"c+d=1", arrow=:none, ls=:dash, lw=2),
		map(cd ->
			V2(first(cd)*v + last(cd)*w; # Using matmul: [v w] * cd
				pt=:point, c=:black, a=L"%$(cd[1])v + %$(cd[2])w",
				ao=[0.5, 0], asz=6), 
			eachrow([C D])
		)...
	)
end

# ╔═╡ 1350d262-9ac3-46c4-85b6-b6c3102e36af
md"""
**17.** Locate $\frac{1}{3}\b{v} + \frac{1}{3}\b{w}$ and $\frac{2}{3}\b{v} + \frac{2}{3}\b{w}$. The combinations $c\b{v}+c\b{w}$ fill out what line?
"""

# ╔═╡ 0182eaeb-953a-4314-9e5d-14be03d2aaa1
let
	v = [6, 1]; w = [1, 6]
	C = -1:0.25:1
	plot(
		V2(v, l=L"v"),
		V2(w, l=L"w"),
		V2(2(v+w); o=-(v+w), l=L"c=d", arrow=:none, ls=:dash, lw=2),
		map(c ->
			V2(c*v + c*w; pt=:point, c=:black, a=L"%$c(v + w)", asz=6), 
			C
		)...
	)
end

# ╔═╡ 747a31e0-b161-40bb-9c3b-70b7238fa898
md"""
**18.** Restricted by $0 \leq c \leq 1$ and $0 \leq d \leq 1$, shade in all combinations $c\b{v} + d\b{w}$.

This area is the parallelogram with points $\b{0}, \b{v}, \b{v}+\b{w}, \b{w}$:
"""

# ╔═╡ eeaf50ba-9f98-4747-afa5-a9ed66bc4d77
let
	v = [6, 1]; w = [1, 6]
	shaded_area = Shape(map(Tuple, [[0, 0], v, v+w, w]))
	plt = plot(
		V2(v, a=L"v", c=1, lw=3),
		V2(w, a=L"w", ao=[0, 0.3], c=2, lw=3),
		V2(v, o=w, c=1, ls=:dash),
		V2(w, o=v, c=2, ls=:dash, a=L"v+w");
		xlim=(0, 8), ylim=(0, 8)
	)
	plot!(shaded_area, fillcolor = plot_color(:gray, 0.3), linecolor=nothing, label=L"cv + dw : 0 \leq c \leq 1, 0 \leq d \leq 1")
	plt
end

# ╔═╡ 3d9b7861-5014-49ec-92dc-4784dfde036c
md"""
**19.** Restricted only b $c \geq 0$ and $d \geq 0$, draw the "cone" of all combinations $c\b{v} + d\b{w}$.
"""

# ╔═╡ 1b5c5a4b-a413-4d05-b220-f3e334e0a3c5
let
	v = [6, 1]; w = [1, 6]
	shaded_area = Shape(map(Tuple, [[0, 0], 4v, 4w]))
	plt = plot(
		V2(v, a=L"v", c=1, lw=3),
		V2(w, a=L"w", c=2, lw=3);
		xlim=(0, 12), ylim=(0, 12)
	)
	plot!(shaded_area, fillcolor = plot_color(:gray, 0.3), linecolor=nothing, label=L"cv + dw : c \geq 0, d \geq 0")
	plt
end

# ╔═╡ 118e1443-63b3-47d3-aa71-c8ed8a385865
md"""
Probs. **20-25** deal with the following $\b{u}, \b{v},$ and $\b{w}$: (The book does not define the vectors precisely, as the lessons work with arbitrary vectors.)
"""

# ╔═╡ b0eec3fe-5a6c-49bb-aed6-6f13e45a68c2


# ╔═╡ 00000000-0000-0000-0000-000000000001
PLUTO_PROJECT_TOML_CONTENTS = """
[deps]
LaTeXStrings = "b964fa9f-0449-5b57-a5c2-d3ea65f4040f"
Plots = "91a5bcdd-55d7-5caf-9e0b-520d859cae80"
StaticArrays = "90137ffa-7385-5640-81b9-e52037218182"

[compat]
LaTeXStrings = "~1.3.0"
Plots = "~1.38.2"
StaticArrays = "~1.5.12"
"""

# ╔═╡ 00000000-0000-0000-0000-000000000002
PLUTO_MANIFEST_TOML_CONTENTS = """
# This file is machine-generated - editing it directly is not advised

julia_version = "1.8.5"
manifest_format = "2.0"
project_hash = "9b91ffee99c6d7741eb19032f03d8d1ac037f9b1"

[[deps.ArgTools]]
uuid = "0dad84c5-d112-42e6-8d28-ef12dabb789f"
version = "1.1.1"

[[deps.Artifacts]]
uuid = "56f22d72-fd6d-98f1-02f0-08ddc0907c33"

[[deps.Base64]]
uuid = "2a0f44e3-6c83-55bd-87e4-b1978d98bd5f"

[[deps.BitFlags]]
git-tree-sha1 = "43b1a4a8f797c1cddadf60499a8a077d4af2cd2d"
uuid = "d1d4a3ce-64b1-5f1a-9ba4-7e7e69966f35"
version = "0.1.7"

[[deps.Bzip2_jll]]
deps = ["Artifacts", "JLLWrappers", "Libdl", "Pkg"]
git-tree-sha1 = "19a35467a82e236ff51bc17a3a44b69ef35185a2"
uuid = "6e34b625-4abd-537c-b88f-471c36dfa7a0"
version = "1.0.8+0"

[[deps.Cairo_jll]]
deps = ["Artifacts", "Bzip2_jll", "CompilerSupportLibraries_jll", "Fontconfig_jll", "FreeType2_jll", "Glib_jll", "JLLWrappers", "LZO_jll", "Libdl", "Pixman_jll", "Pkg", "Xorg_libXext_jll", "Xorg_libXrender_jll", "Zlib_jll", "libpng_jll"]
git-tree-sha1 = "4b859a208b2397a7a623a03449e4636bdb17bcf2"
uuid = "83423d85-b0ee-5818-9007-b63ccbeb887a"
version = "1.16.1+1"

[[deps.ChainRulesCore]]
deps = ["Compat", "LinearAlgebra", "SparseArrays"]
git-tree-sha1 = "e7ff6cadf743c098e08fca25c91103ee4303c9bb"
uuid = "d360d2e6-b24c-11e9-a2a3-2a2ae2dbcce4"
version = "1.15.6"

[[deps.ChangesOfVariables]]
deps = ["ChainRulesCore", "LinearAlgebra", "Test"]
git-tree-sha1 = "38f7a08f19d8810338d4f5085211c7dfa5d5bdd8"
uuid = "9e997f8a-9a97-42d5-a9f1-ce6bfc15e2c0"
version = "0.1.4"

[[deps.CodecZlib]]
deps = ["TranscodingStreams", "Zlib_jll"]
git-tree-sha1 = "ded953804d019afa9a3f98981d99b33e3db7b6da"
uuid = "944b1d66-785c-5afd-91f1-9de20f533193"
version = "0.7.0"

[[deps.ColorSchemes]]
deps = ["ColorTypes", "ColorVectorSpace", "Colors", "FixedPointNumbers", "Random", "SnoopPrecompile"]
git-tree-sha1 = "aa3edc8f8dea6cbfa176ee12f7c2fc82f0608ed3"
uuid = "35d6a980-a343-548e-a6ea-1d62b119f2f4"
version = "3.20.0"

[[deps.ColorTypes]]
deps = ["FixedPointNumbers", "Random"]
git-tree-sha1 = "eb7f0f8307f71fac7c606984ea5fb2817275d6e4"
uuid = "3da002f7-5984-5a60-b8a6-cbb66c0b333f"
version = "0.11.4"

[[deps.ColorVectorSpace]]
deps = ["ColorTypes", "FixedPointNumbers", "LinearAlgebra", "SpecialFunctions", "Statistics", "TensorCore"]
git-tree-sha1 = "600cc5508d66b78aae350f7accdb58763ac18589"
uuid = "c3611d14-8923-5661-9e6a-0046d554d3a4"
version = "0.9.10"

[[deps.Colors]]
deps = ["ColorTypes", "FixedPointNumbers", "Reexport"]
git-tree-sha1 = "fc08e5930ee9a4e03f84bfb5211cb54e7769758a"
uuid = "5ae59095-9a9b-59fe-a467-6f913c188581"
version = "0.12.10"

[[deps.Compat]]
deps = ["Dates", "LinearAlgebra", "UUIDs"]
git-tree-sha1 = "00a2cccc7f098ff3b66806862d275ca3db9e6e5a"
uuid = "34da2185-b29b-5c13-b0c7-acf172513d20"
version = "4.5.0"

[[deps.CompilerSupportLibraries_jll]]
deps = ["Artifacts", "Libdl"]
uuid = "e66e0078-7015-5450-92f7-15fbd957f2ae"
version = "1.0.1+0"

[[deps.Contour]]
git-tree-sha1 = "d05d9e7b7aedff4e5b51a029dced05cfb6125781"
uuid = "d38c429a-6771-53c6-b99e-75d170b6e991"
version = "0.6.2"

[[deps.DataAPI]]
git-tree-sha1 = "e8119c1a33d267e16108be441a287a6981ba1630"
uuid = "9a962f9c-6df0-11e9-0e5d-c546b8b5ee8a"
version = "1.14.0"

[[deps.DataStructures]]
deps = ["Compat", "InteractiveUtils", "OrderedCollections"]
git-tree-sha1 = "d1fff3a548102f48987a52a2e0d114fa97d730f0"
uuid = "864edb3b-99cc-5e75-8d2d-829cb0a9cfe8"
version = "0.18.13"

[[deps.Dates]]
deps = ["Printf"]
uuid = "ade2ca70-3891-5945-98fb-dc099432e06a"

[[deps.DelimitedFiles]]
deps = ["Mmap"]
uuid = "8bb1440f-4735-579b-a4ab-409b98df4dab"

[[deps.DocStringExtensions]]
deps = ["LibGit2"]
git-tree-sha1 = "2fb1e02f2b635d0845df5d7c167fec4dd739b00d"
uuid = "ffbed154-4ef7-542d-bbb7-c09d3a79fcae"
version = "0.9.3"

[[deps.Downloads]]
deps = ["ArgTools", "FileWatching", "LibCURL", "NetworkOptions"]
uuid = "f43a241f-c20a-4ad4-852c-f6b1247861c6"
version = "1.6.0"

[[deps.Expat_jll]]
deps = ["Artifacts", "JLLWrappers", "Libdl", "Pkg"]
git-tree-sha1 = "bad72f730e9e91c08d9427d5e8db95478a3c323d"
uuid = "2e619515-83b5-522b-bb60-26c02a35a201"
version = "2.4.8+0"

[[deps.FFMPEG]]
deps = ["FFMPEG_jll"]
git-tree-sha1 = "b57e3acbe22f8484b4b5ff66a7499717fe1a9cc8"
uuid = "c87230d0-a227-11e9-1b43-d7ebe4e7570a"
version = "0.4.1"

[[deps.FFMPEG_jll]]
deps = ["Artifacts", "Bzip2_jll", "FreeType2_jll", "FriBidi_jll", "JLLWrappers", "LAME_jll", "Libdl", "Ogg_jll", "OpenSSL_jll", "Opus_jll", "PCRE2_jll", "Pkg", "Zlib_jll", "libaom_jll", "libass_jll", "libfdk_aac_jll", "libvorbis_jll", "x264_jll", "x265_jll"]
git-tree-sha1 = "74faea50c1d007c85837327f6775bea60b5492dd"
uuid = "b22a6f82-2f65-5046-a5b2-351ab43fb4e5"
version = "4.4.2+2"

[[deps.FileWatching]]
uuid = "7b1f6079-737a-58dc-b8bc-7a2ca5c1b5ee"

[[deps.FixedPointNumbers]]
deps = ["Statistics"]
git-tree-sha1 = "335bfdceacc84c5cdf16aadc768aa5ddfc5383cc"
uuid = "53c48c17-4a7d-5ca2-90c5-79b7896eea93"
version = "0.8.4"

[[deps.Fontconfig_jll]]
deps = ["Artifacts", "Bzip2_jll", "Expat_jll", "FreeType2_jll", "JLLWrappers", "Libdl", "Libuuid_jll", "Pkg", "Zlib_jll"]
git-tree-sha1 = "21efd19106a55620a188615da6d3d06cd7f6ee03"
uuid = "a3f928ae-7b40-5064-980b-68af3947d34b"
version = "2.13.93+0"

[[deps.Formatting]]
deps = ["Printf"]
git-tree-sha1 = "8339d61043228fdd3eb658d86c926cb282ae72a8"
uuid = "59287772-0a20-5a39-b81b-1366585eb4c0"
version = "0.4.2"

[[deps.FreeType2_jll]]
deps = ["Artifacts", "Bzip2_jll", "JLLWrappers", "Libdl", "Pkg", "Zlib_jll"]
git-tree-sha1 = "87eb71354d8ec1a96d4a7636bd57a7347dde3ef9"
uuid = "d7e528f0-a631-5988-bf34-fe36492bcfd7"
version = "2.10.4+0"

[[deps.FriBidi_jll]]
deps = ["Artifacts", "JLLWrappers", "Libdl", "Pkg"]
git-tree-sha1 = "aa31987c2ba8704e23c6c8ba8a4f769d5d7e4f91"
uuid = "559328eb-81f9-559d-9380-de523a88c83c"
version = "1.0.10+0"

[[deps.GLFW_jll]]
deps = ["Artifacts", "JLLWrappers", "Libdl", "Libglvnd_jll", "Pkg", "Xorg_libXcursor_jll", "Xorg_libXi_jll", "Xorg_libXinerama_jll", "Xorg_libXrandr_jll"]
git-tree-sha1 = "d972031d28c8c8d9d7b41a536ad7bb0c2579caca"
uuid = "0656b61e-2033-5cc2-a64a-77c0f6c09b89"
version = "3.3.8+0"

[[deps.GR]]
deps = ["Artifacts", "Base64", "DelimitedFiles", "Downloads", "GR_jll", "HTTP", "JSON", "Libdl", "LinearAlgebra", "Pkg", "Preferences", "Printf", "Random", "Serialization", "Sockets", "TOML", "Tar", "Test", "UUIDs", "p7zip_jll"]
git-tree-sha1 = "387d2b8b3ca57b791633f0993b31d8cb43ea3292"
uuid = "28b8d3ca-fb5f-59d9-8090-bfdbd6d07a71"
version = "0.71.3"

[[deps.GR_jll]]
deps = ["Artifacts", "Bzip2_jll", "Cairo_jll", "FFMPEG_jll", "Fontconfig_jll", "GLFW_jll", "JLLWrappers", "JpegTurbo_jll", "Libdl", "Libtiff_jll", "Pixman_jll", "Pkg", "Qt5Base_jll", "Zlib_jll", "libpng_jll"]
git-tree-sha1 = "5982b5e20f97bff955e9a2343a14da96a746cd8c"
uuid = "d2c73de3-f751-5644-a686-071e5b155ba9"
version = "0.71.3+0"

[[deps.Gettext_jll]]
deps = ["Artifacts", "CompilerSupportLibraries_jll", "JLLWrappers", "Libdl", "Libiconv_jll", "Pkg", "XML2_jll"]
git-tree-sha1 = "9b02998aba7bf074d14de89f9d37ca24a1a0b046"
uuid = "78b55507-aeef-58d4-861c-77aaff3498b1"
version = "0.21.0+0"

[[deps.Glib_jll]]
deps = ["Artifacts", "Gettext_jll", "JLLWrappers", "Libdl", "Libffi_jll", "Libiconv_jll", "Libmount_jll", "PCRE2_jll", "Pkg", "Zlib_jll"]
git-tree-sha1 = "d3b3624125c1474292d0d8ed0f65554ac37ddb23"
uuid = "7746bdde-850d-59dc-9ae8-88ece973131d"
version = "2.74.0+2"

[[deps.Graphite2_jll]]
deps = ["Artifacts", "JLLWrappers", "Libdl", "Pkg"]
git-tree-sha1 = "344bf40dcab1073aca04aa0df4fb092f920e4011"
uuid = "3b182d85-2403-5c21-9c21-1e1f0cc25472"
version = "1.3.14+0"

[[deps.Grisu]]
git-tree-sha1 = "53bb909d1151e57e2484c3d1b53e19552b887fb2"
uuid = "42e2da0e-8278-4e71-bc24-59509adca0fe"
version = "1.0.2"

[[deps.HTTP]]
deps = ["Base64", "CodecZlib", "Dates", "IniFile", "Logging", "LoggingExtras", "MbedTLS", "NetworkOptions", "OpenSSL", "Random", "SimpleBufferStream", "Sockets", "URIs", "UUIDs"]
git-tree-sha1 = "eb5aa5e3b500e191763d35198f859e4b40fff4a6"
uuid = "cd3eb016-35fb-5094-929b-558a96fad6f3"
version = "1.7.3"

[[deps.HarfBuzz_jll]]
deps = ["Artifacts", "Cairo_jll", "Fontconfig_jll", "FreeType2_jll", "Glib_jll", "Graphite2_jll", "JLLWrappers", "Libdl", "Libffi_jll", "Pkg"]
git-tree-sha1 = "129acf094d168394e80ee1dc4bc06ec835e510a3"
uuid = "2e76f6c2-a576-52d4-95c1-20adfe4de566"
version = "2.8.1+1"

[[deps.IniFile]]
git-tree-sha1 = "f550e6e32074c939295eb5ea6de31849ac2c9625"
uuid = "83e8ac13-25f8-5344-8a64-a9f2b223428f"
version = "0.5.1"

[[deps.InteractiveUtils]]
deps = ["Markdown"]
uuid = "b77e0a4c-d291-57a0-90e8-8db25a27a240"

[[deps.InverseFunctions]]
deps = ["Test"]
git-tree-sha1 = "49510dfcb407e572524ba94aeae2fced1f3feb0f"
uuid = "3587e190-3f89-42d0-90ee-14403ec27112"
version = "0.1.8"

[[deps.IrrationalConstants]]
git-tree-sha1 = "7fd44fd4ff43fc60815f8e764c0f352b83c49151"
uuid = "92d709cd-6900-40b7-9082-c6be49f344b6"
version = "0.1.1"

[[deps.JLFzf]]
deps = ["Pipe", "REPL", "Random", "fzf_jll"]
git-tree-sha1 = "f377670cda23b6b7c1c0b3893e37451c5c1a2185"
uuid = "1019f520-868f-41f5-a6de-eb00f4b6a39c"
version = "0.1.5"

[[deps.JLLWrappers]]
deps = ["Preferences"]
git-tree-sha1 = "abc9885a7ca2052a736a600f7fa66209f96506e1"
uuid = "692b3bcd-3c85-4b1f-b108-f13ce0eb3210"
version = "1.4.1"

[[deps.JSON]]
deps = ["Dates", "Mmap", "Parsers", "Unicode"]
git-tree-sha1 = "3c837543ddb02250ef42f4738347454f95079d4e"
uuid = "682c06a0-de6a-54ab-a142-c8b1cf79cde6"
version = "0.21.3"

[[deps.JpegTurbo_jll]]
deps = ["Artifacts", "JLLWrappers", "Libdl", "Pkg"]
git-tree-sha1 = "b53380851c6e6664204efb2e62cd24fa5c47e4ba"
uuid = "aacddb02-875f-59d6-b918-886e6ef4fbf8"
version = "2.1.2+0"

[[deps.LAME_jll]]
deps = ["Artifacts", "JLLWrappers", "Libdl", "Pkg"]
git-tree-sha1 = "f6250b16881adf048549549fba48b1161acdac8c"
uuid = "c1c5ebd0-6772-5130-a774-d5fcae4a789d"
version = "3.100.1+0"

[[deps.LERC_jll]]
deps = ["Artifacts", "JLLWrappers", "Libdl", "Pkg"]
git-tree-sha1 = "bf36f528eec6634efc60d7ec062008f171071434"
uuid = "88015f11-f218-50d7-93a8-a6af411a945d"
version = "3.0.0+1"

[[deps.LZO_jll]]
deps = ["Artifacts", "JLLWrappers", "Libdl", "Pkg"]
git-tree-sha1 = "e5b909bcf985c5e2605737d2ce278ed791b89be6"
uuid = "dd4b983a-f0e5-5f8d-a1b7-129d4a5fb1ac"
version = "2.10.1+0"

[[deps.LaTeXStrings]]
git-tree-sha1 = "f2355693d6778a178ade15952b7ac47a4ff97996"
uuid = "b964fa9f-0449-5b57-a5c2-d3ea65f4040f"
version = "1.3.0"

[[deps.Latexify]]
deps = ["Formatting", "InteractiveUtils", "LaTeXStrings", "MacroTools", "Markdown", "OrderedCollections", "Printf", "Requires"]
git-tree-sha1 = "2422f47b34d4b127720a18f86fa7b1aa2e141f29"
uuid = "23fbe1c1-3f47-55db-b15f-69d7ec21a316"
version = "0.15.18"

[[deps.LibCURL]]
deps = ["LibCURL_jll", "MozillaCACerts_jll"]
uuid = "b27032c2-a3e7-50c8-80cd-2d36dbcbfd21"
version = "0.6.3"

[[deps.LibCURL_jll]]
deps = ["Artifacts", "LibSSH2_jll", "Libdl", "MbedTLS_jll", "Zlib_jll", "nghttp2_jll"]
uuid = "deac9b47-8bc7-5906-a0fe-35ac56dc84c0"
version = "7.84.0+0"

[[deps.LibGit2]]
deps = ["Base64", "NetworkOptions", "Printf", "SHA"]
uuid = "76f85450-5226-5b5a-8eaa-529ad045b433"

[[deps.LibSSH2_jll]]
deps = ["Artifacts", "Libdl", "MbedTLS_jll"]
uuid = "29816b5a-b9ab-546f-933c-edad1886dfa8"
version = "1.10.2+0"

[[deps.Libdl]]
uuid = "8f399da3-3557-5675-b5ff-fb832c97cbdb"

[[deps.Libffi_jll]]
deps = ["Artifacts", "JLLWrappers", "Libdl", "Pkg"]
git-tree-sha1 = "0b4a5d71f3e5200a7dff793393e09dfc2d874290"
uuid = "e9f186c6-92d2-5b65-8a66-fee21dc1b490"
version = "3.2.2+1"

[[deps.Libgcrypt_jll]]
deps = ["Artifacts", "JLLWrappers", "Libdl", "Libgpg_error_jll", "Pkg"]
git-tree-sha1 = "64613c82a59c120435c067c2b809fc61cf5166ae"
uuid = "d4300ac3-e22c-5743-9152-c294e39db1e4"
version = "1.8.7+0"

[[deps.Libglvnd_jll]]
deps = ["Artifacts", "JLLWrappers", "Libdl", "Pkg", "Xorg_libX11_jll", "Xorg_libXext_jll"]
git-tree-sha1 = "6f73d1dd803986947b2c750138528a999a6c7733"
uuid = "7e76a0d4-f3c7-5321-8279-8d96eeed0f29"
version = "1.6.0+0"

[[deps.Libgpg_error_jll]]
deps = ["Artifacts", "JLLWrappers", "Libdl", "Pkg"]
git-tree-sha1 = "c333716e46366857753e273ce6a69ee0945a6db9"
uuid = "7add5ba3-2f88-524e-9cd5-f83b8a55f7b8"
version = "1.42.0+0"

[[deps.Libiconv_jll]]
deps = ["Artifacts", "JLLWrappers", "Libdl", "Pkg"]
git-tree-sha1 = "c7cb1f5d892775ba13767a87c7ada0b980ea0a71"
uuid = "94ce4f54-9a6c-5748-9c1c-f9c7231a4531"
version = "1.16.1+2"

[[deps.Libmount_jll]]
deps = ["Artifacts", "JLLWrappers", "Libdl", "Pkg"]
git-tree-sha1 = "9c30530bf0effd46e15e0fdcf2b8636e78cbbd73"
uuid = "4b2f31a3-9ecc-558c-b454-b3730dcb73e9"
version = "2.35.0+0"

[[deps.Libtiff_jll]]
deps = ["Artifacts", "JLLWrappers", "JpegTurbo_jll", "LERC_jll", "Libdl", "Pkg", "Zlib_jll", "Zstd_jll"]
git-tree-sha1 = "3eb79b0ca5764d4799c06699573fd8f533259713"
uuid = "89763e89-9b03-5906-acba-b20f662cd828"
version = "4.4.0+0"

[[deps.Libuuid_jll]]
deps = ["Artifacts", "JLLWrappers", "Libdl", "Pkg"]
git-tree-sha1 = "7f3efec06033682db852f8b3bc3c1d2b0a0ab066"
uuid = "38a345b3-de98-5d2b-a5d3-14cd9215e700"
version = "2.36.0+0"

[[deps.LinearAlgebra]]
deps = ["Libdl", "libblastrampoline_jll"]
uuid = "37e2e46d-f89d-539d-b4ee-838fcccc9c8e"

[[deps.LogExpFunctions]]
deps = ["ChainRulesCore", "ChangesOfVariables", "DocStringExtensions", "InverseFunctions", "IrrationalConstants", "LinearAlgebra"]
git-tree-sha1 = "946607f84feb96220f480e0422d3484c49c00239"
uuid = "2ab3a3ac-af41-5b50-aa03-7779005ae688"
version = "0.3.19"

[[deps.Logging]]
uuid = "56ddb016-857b-54e1-b83d-db4d58db5568"

[[deps.LoggingExtras]]
deps = ["Dates", "Logging"]
git-tree-sha1 = "cedb76b37bc5a6c702ade66be44f831fa23c681e"
uuid = "e6f89c97-d47a-5376-807f-9c37f3926c36"
version = "1.0.0"

[[deps.MacroTools]]
deps = ["Markdown", "Random"]
git-tree-sha1 = "42324d08725e200c23d4dfb549e0d5d89dede2d2"
uuid = "1914dd2f-81c6-5fcd-8719-6d5c9610ff09"
version = "0.5.10"

[[deps.Markdown]]
deps = ["Base64"]
uuid = "d6f4376e-aef5-505a-96c1-9c027394607a"

[[deps.MbedTLS]]
deps = ["Dates", "MbedTLS_jll", "MozillaCACerts_jll", "Random", "Sockets"]
git-tree-sha1 = "03a9b9718f5682ecb107ac9f7308991db4ce395b"
uuid = "739be429-bea8-5141-9913-cc70e7f3736d"
version = "1.1.7"

[[deps.MbedTLS_jll]]
deps = ["Artifacts", "Libdl"]
uuid = "c8ffd9c3-330d-5841-b78e-0817d7145fa1"
version = "2.28.0+0"

[[deps.Measures]]
git-tree-sha1 = "c13304c81eec1ed3af7fc20e75fb6b26092a1102"
uuid = "442fdcdd-2543-5da2-b0f3-8c86c306513e"
version = "0.3.2"

[[deps.Missings]]
deps = ["DataAPI"]
git-tree-sha1 = "f66bdc5de519e8f8ae43bdc598782d35a25b1272"
uuid = "e1d29d7a-bbdc-5cf2-9ac0-f12de2c33e28"
version = "1.1.0"

[[deps.Mmap]]
uuid = "a63ad114-7e13-5084-954f-fe012c677804"

[[deps.MozillaCACerts_jll]]
uuid = "14a3606d-f60d-562e-9121-12d972cd8159"
version = "2022.2.1"

[[deps.NaNMath]]
deps = ["OpenLibm_jll"]
git-tree-sha1 = "a7c3d1da1189a1c2fe843a3bfa04d18d20eb3211"
uuid = "77ba4419-2d1f-58cd-9bb1-8ffee604a2e3"
version = "1.0.1"

[[deps.NetworkOptions]]
uuid = "ca575930-c2e3-43a9-ace4-1e988b2c1908"
version = "1.2.0"

[[deps.Ogg_jll]]
deps = ["Artifacts", "JLLWrappers", "Libdl", "Pkg"]
git-tree-sha1 = "887579a3eb005446d514ab7aeac5d1d027658b8f"
uuid = "e7412a2a-1a6e-54c0-be00-318e2571c051"
version = "1.3.5+1"

[[deps.OpenBLAS_jll]]
deps = ["Artifacts", "CompilerSupportLibraries_jll", "Libdl"]
uuid = "4536629a-c528-5b80-bd46-f80d51c5b363"
version = "0.3.20+0"

[[deps.OpenLibm_jll]]
deps = ["Artifacts", "Libdl"]
uuid = "05823500-19ac-5b8b-9628-191a04bc5112"
version = "0.8.1+0"

[[deps.OpenSSL]]
deps = ["BitFlags", "Dates", "MozillaCACerts_jll", "OpenSSL_jll", "Sockets"]
git-tree-sha1 = "6503b77492fd7fcb9379bf73cd31035670e3c509"
uuid = "4d8831e6-92b7-49fb-bdf8-b643e874388c"
version = "1.3.3"

[[deps.OpenSSL_jll]]
deps = ["Artifacts", "JLLWrappers", "Libdl", "Pkg"]
git-tree-sha1 = "f6e9dba33f9f2c44e08a020b0caf6903be540004"
uuid = "458c3c95-2e84-50aa-8efc-19380b2a3a95"
version = "1.1.19+0"

[[deps.OpenSpecFun_jll]]
deps = ["Artifacts", "CompilerSupportLibraries_jll", "JLLWrappers", "Libdl", "Pkg"]
git-tree-sha1 = "13652491f6856acfd2db29360e1bbcd4565d04f1"
uuid = "efe28fd5-8261-553b-a9e1-b2916fc3738e"
version = "0.5.5+0"

[[deps.Opus_jll]]
deps = ["Artifacts", "JLLWrappers", "Libdl", "Pkg"]
git-tree-sha1 = "51a08fb14ec28da2ec7a927c4337e4332c2a4720"
uuid = "91d4177d-7536-5919-b921-800302f37372"
version = "1.3.2+0"

[[deps.OrderedCollections]]
git-tree-sha1 = "85f8e6578bf1f9ee0d11e7bb1b1456435479d47c"
uuid = "bac558e1-5e72-5ebc-8fee-abe8a469f55d"
version = "1.4.1"

[[deps.PCRE2_jll]]
deps = ["Artifacts", "Libdl"]
uuid = "efcefdf7-47ab-520b-bdef-62a2eaa19f15"
version = "10.40.0+0"

[[deps.Parsers]]
deps = ["Dates", "SnoopPrecompile"]
git-tree-sha1 = "8175fc2b118a3755113c8e68084dc1a9e63c61ee"
uuid = "69de0a69-1ddd-5017-9359-2bf0b02dc9f0"
version = "2.5.3"

[[deps.Pipe]]
git-tree-sha1 = "6842804e7867b115ca9de748a0cf6b364523c16d"
uuid = "b98c9c47-44ae-5843-9183-064241ee97a0"
version = "1.3.0"

[[deps.Pixman_jll]]
deps = ["Artifacts", "JLLWrappers", "Libdl", "Pkg"]
git-tree-sha1 = "b4f5d02549a10e20780a24fce72bea96b6329e29"
uuid = "30392449-352a-5448-841d-b1acce4e97dc"
version = "0.40.1+0"

[[deps.Pkg]]
deps = ["Artifacts", "Dates", "Downloads", "LibGit2", "Libdl", "Logging", "Markdown", "Printf", "REPL", "Random", "SHA", "Serialization", "TOML", "Tar", "UUIDs", "p7zip_jll"]
uuid = "44cfe95a-1eb2-52ea-b672-e2afdf69b78f"
version = "1.8.0"

[[deps.PlotThemes]]
deps = ["PlotUtils", "Statistics"]
git-tree-sha1 = "1f03a2d339f42dca4a4da149c7e15e9b896ad899"
uuid = "ccf2f8ad-2431-5c83-bf29-c5338b663b6a"
version = "3.1.0"

[[deps.PlotUtils]]
deps = ["ColorSchemes", "Colors", "Dates", "Printf", "Random", "Reexport", "SnoopPrecompile", "Statistics"]
git-tree-sha1 = "5b7690dd212e026bbab1860016a6601cb077ab66"
uuid = "995b91a9-d308-5afd-9ec6-746e21dbc043"
version = "1.3.2"

[[deps.Plots]]
deps = ["Base64", "Contour", "Dates", "Downloads", "FFMPEG", "FixedPointNumbers", "GR", "JLFzf", "JSON", "LaTeXStrings", "Latexify", "LinearAlgebra", "Measures", "NaNMath", "Pkg", "PlotThemes", "PlotUtils", "Preferences", "Printf", "REPL", "Random", "RecipesBase", "RecipesPipeline", "Reexport", "RelocatableFolders", "Requires", "Scratch", "Showoff", "SnoopPrecompile", "SparseArrays", "Statistics", "StatsBase", "UUIDs", "UnicodeFun", "Unzip"]
git-tree-sha1 = "a99bbd3664bb12a775cda2eba7f3b2facf3dad94"
uuid = "91a5bcdd-55d7-5caf-9e0b-520d859cae80"
version = "1.38.2"

[[deps.Preferences]]
deps = ["TOML"]
git-tree-sha1 = "47e5f437cc0e7ef2ce8406ce1e7e24d44915f88d"
uuid = "21216c6a-2e73-6563-6e65-726566657250"
version = "1.3.0"

[[deps.Printf]]
deps = ["Unicode"]
uuid = "de0858da-6303-5e67-8744-51eddeeeb8d7"

[[deps.Qt5Base_jll]]
deps = ["Artifacts", "CompilerSupportLibraries_jll", "Fontconfig_jll", "Glib_jll", "JLLWrappers", "Libdl", "Libglvnd_jll", "OpenSSL_jll", "Pkg", "Xorg_libXext_jll", "Xorg_libxcb_jll", "Xorg_xcb_util_image_jll", "Xorg_xcb_util_keysyms_jll", "Xorg_xcb_util_renderutil_jll", "Xorg_xcb_util_wm_jll", "Zlib_jll", "xkbcommon_jll"]
git-tree-sha1 = "0c03844e2231e12fda4d0086fd7cbe4098ee8dc5"
uuid = "ea2cea3b-5b76-57ae-a6ef-0a8af62496e1"
version = "5.15.3+2"

[[deps.REPL]]
deps = ["InteractiveUtils", "Markdown", "Sockets", "Unicode"]
uuid = "3fa0cd96-eef1-5676-8a61-b3b8758bbffb"

[[deps.Random]]
deps = ["SHA", "Serialization"]
uuid = "9a3f8284-a2c9-5f02-9a11-845980a1fd5c"

[[deps.RecipesBase]]
deps = ["SnoopPrecompile"]
git-tree-sha1 = "261dddd3b862bd2c940cf6ca4d1c8fe593e457c8"
uuid = "3cdcf5f2-1ef4-517c-9805-6587b60abb01"
version = "1.3.3"

[[deps.RecipesPipeline]]
deps = ["Dates", "NaNMath", "PlotUtils", "RecipesBase", "SnoopPrecompile"]
git-tree-sha1 = "e974477be88cb5e3040009f3767611bc6357846f"
uuid = "01d81517-befc-4cb6-b9ec-a95719d0359c"
version = "0.6.11"

[[deps.Reexport]]
git-tree-sha1 = "45e428421666073eab6f2da5c9d310d99bb12f9b"
uuid = "189a3867-3050-52da-a836-e630ba90ab69"
version = "1.2.2"

[[deps.RelocatableFolders]]
deps = ["SHA", "Scratch"]
git-tree-sha1 = "90bc7a7c96410424509e4263e277e43250c05691"
uuid = "05181044-ff0b-4ac5-8273-598c1e38db00"
version = "1.0.0"

[[deps.Requires]]
deps = ["UUIDs"]
git-tree-sha1 = "838a3a4188e2ded87a4f9f184b4b0d78a1e91cb7"
uuid = "ae029012-a4dd-5104-9daa-d747884805df"
version = "1.3.0"

[[deps.SHA]]
uuid = "ea8e919c-243c-51af-8825-aaa63cd721ce"
version = "0.7.0"

[[deps.Scratch]]
deps = ["Dates"]
git-tree-sha1 = "f94f779c94e58bf9ea243e77a37e16d9de9126bd"
uuid = "6c6a2e73-6563-6170-7368-637461726353"
version = "1.1.1"

[[deps.Serialization]]
uuid = "9e88b42a-f829-5b0c-bbe9-9e923198166b"

[[deps.Showoff]]
deps = ["Dates", "Grisu"]
git-tree-sha1 = "91eddf657aca81df9ae6ceb20b959ae5653ad1de"
uuid = "992d4aef-0814-514b-bc4d-f2e9a6c4116f"
version = "1.0.3"

[[deps.SimpleBufferStream]]
git-tree-sha1 = "874e8867b33a00e784c8a7e4b60afe9e037b74e1"
uuid = "777ac1f9-54b0-4bf8-805c-2214025038e7"
version = "1.1.0"

[[deps.SnoopPrecompile]]
deps = ["Preferences"]
git-tree-sha1 = "e760a70afdcd461cf01a575947738d359234665c"
uuid = "66db9d55-30c0-4569-8b51-7e840670fc0c"
version = "1.0.3"

[[deps.Sockets]]
uuid = "6462fe0b-24de-5631-8697-dd941f90decc"

[[deps.SortingAlgorithms]]
deps = ["DataStructures"]
git-tree-sha1 = "a4ada03f999bd01b3a25dcaa30b2d929fe537e00"
uuid = "a2af1166-a08f-5f64-846c-94a0d3cef48c"
version = "1.1.0"

[[deps.SparseArrays]]
deps = ["LinearAlgebra", "Random"]
uuid = "2f01184e-e22b-5df5-ae63-d93ebab69eaf"

[[deps.SpecialFunctions]]
deps = ["ChainRulesCore", "IrrationalConstants", "LogExpFunctions", "OpenLibm_jll", "OpenSpecFun_jll"]
git-tree-sha1 = "d75bda01f8c31ebb72df80a46c88b25d1c79c56d"
uuid = "276daf66-3868-5448-9aa4-cd146d93841b"
version = "2.1.7"

[[deps.StaticArrays]]
deps = ["LinearAlgebra", "Random", "StaticArraysCore", "Statistics"]
git-tree-sha1 = "6954a456979f23d05085727adb17c4551c19ecd1"
uuid = "90137ffa-7385-5640-81b9-e52037218182"
version = "1.5.12"

[[deps.StaticArraysCore]]
git-tree-sha1 = "6b7ba252635a5eff6a0b0664a41ee140a1c9e72a"
uuid = "1e83bf80-4336-4d27-bf5d-d5a4f845583c"
version = "1.4.0"

[[deps.Statistics]]
deps = ["LinearAlgebra", "SparseArrays"]
uuid = "10745b16-79ce-11e8-11f9-7d13ad32a3b2"

[[deps.StatsAPI]]
deps = ["LinearAlgebra"]
git-tree-sha1 = "f9af7f195fb13589dd2e2d57fdb401717d2eb1f6"
uuid = "82ae8749-77ed-4fe6-ae5f-f523153014b0"
version = "1.5.0"

[[deps.StatsBase]]
deps = ["DataAPI", "DataStructures", "LinearAlgebra", "LogExpFunctions", "Missings", "Printf", "Random", "SortingAlgorithms", "SparseArrays", "Statistics", "StatsAPI"]
git-tree-sha1 = "d1bf48bfcc554a3761a133fe3a9bb01488e06916"
uuid = "2913bbd2-ae8a-5f71-8c99-4fb6c76f3a91"
version = "0.33.21"

[[deps.TOML]]
deps = ["Dates"]
uuid = "fa267f1f-6049-4f14-aa54-33bafae1ed76"
version = "1.0.0"

[[deps.Tar]]
deps = ["ArgTools", "SHA"]
uuid = "a4e569a6-e804-4fa4-b0f3-eef7a1d5b13e"
version = "1.10.1"

[[deps.TensorCore]]
deps = ["LinearAlgebra"]
git-tree-sha1 = "1feb45f88d133a655e001435632f019a9a1bcdb6"
uuid = "62fd8b95-f654-4bbd-a8a5-9c27f68ccd50"
version = "0.1.1"

[[deps.Test]]
deps = ["InteractiveUtils", "Logging", "Random", "Serialization"]
uuid = "8dfed614-e22c-5e08-85e1-65c5234f0b40"

[[deps.TranscodingStreams]]
deps = ["Random", "Test"]
git-tree-sha1 = "94f38103c984f89cf77c402f2a68dbd870f8165f"
uuid = "3bb67fe8-82b1-5028-8e26-92a6c54297fa"
version = "0.9.11"

[[deps.URIs]]
git-tree-sha1 = "ac00576f90d8a259f2c9d823e91d1de3fd44d348"
uuid = "5c2747f8-b7ea-4ff2-ba2e-563bfd36b1d4"
version = "1.4.1"

[[deps.UUIDs]]
deps = ["Random", "SHA"]
uuid = "cf7118a7-6976-5b1a-9a39-7adc72f591a4"

[[deps.Unicode]]
uuid = "4ec0a83e-493e-50e2-b9ac-8f72acf5a8f5"

[[deps.UnicodeFun]]
deps = ["REPL"]
git-tree-sha1 = "53915e50200959667e78a92a418594b428dffddf"
uuid = "1cfade01-22cf-5700-b092-accc4b62d6e1"
version = "0.4.1"

[[deps.Unzip]]
git-tree-sha1 = "ca0969166a028236229f63514992fc073799bb78"
uuid = "41fe7b60-77ed-43a1-b4f0-825fd5a5650d"
version = "0.2.0"

[[deps.Wayland_jll]]
deps = ["Artifacts", "Expat_jll", "JLLWrappers", "Libdl", "Libffi_jll", "Pkg", "XML2_jll"]
git-tree-sha1 = "ed8d92d9774b077c53e1da50fd81a36af3744c1c"
uuid = "a2964d1f-97da-50d4-b82a-358c7fce9d89"
version = "1.21.0+0"

[[deps.Wayland_protocols_jll]]
deps = ["Artifacts", "JLLWrappers", "Libdl", "Pkg"]
git-tree-sha1 = "4528479aa01ee1b3b4cd0e6faef0e04cf16466da"
uuid = "2381bf8a-dfd0-557d-9999-79630e7b1b91"
version = "1.25.0+0"

[[deps.XML2_jll]]
deps = ["Artifacts", "JLLWrappers", "Libdl", "Libiconv_jll", "Pkg", "Zlib_jll"]
git-tree-sha1 = "93c41695bc1c08c46c5899f4fe06d6ead504bb73"
uuid = "02c8fc9c-b97f-50b9-bbe4-9be30ff0a78a"
version = "2.10.3+0"

[[deps.XSLT_jll]]
deps = ["Artifacts", "JLLWrappers", "Libdl", "Libgcrypt_jll", "Libgpg_error_jll", "Libiconv_jll", "Pkg", "XML2_jll", "Zlib_jll"]
git-tree-sha1 = "91844873c4085240b95e795f692c4cec4d805f8a"
uuid = "aed1982a-8fda-507f-9586-7b0439959a61"
version = "1.1.34+0"

[[deps.Xorg_libX11_jll]]
deps = ["Artifacts", "JLLWrappers", "Libdl", "Pkg", "Xorg_libxcb_jll", "Xorg_xtrans_jll"]
git-tree-sha1 = "5be649d550f3f4b95308bf0183b82e2582876527"
uuid = "4f6342f7-b3d2-589e-9d20-edeb45f2b2bc"
version = "1.6.9+4"

[[deps.Xorg_libXau_jll]]
deps = ["Artifacts", "JLLWrappers", "Libdl", "Pkg"]
git-tree-sha1 = "4e490d5c960c314f33885790ed410ff3a94ce67e"
uuid = "0c0b7dd1-d40b-584c-a123-a41640f87eec"
version = "1.0.9+4"

[[deps.Xorg_libXcursor_jll]]
deps = ["Artifacts", "JLLWrappers", "Libdl", "Pkg", "Xorg_libXfixes_jll", "Xorg_libXrender_jll"]
git-tree-sha1 = "12e0eb3bc634fa2080c1c37fccf56f7c22989afd"
uuid = "935fb764-8cf2-53bf-bb30-45bb1f8bf724"
version = "1.2.0+4"

[[deps.Xorg_libXdmcp_jll]]
deps = ["Artifacts", "JLLWrappers", "Libdl", "Pkg"]
git-tree-sha1 = "4fe47bd2247248125c428978740e18a681372dd4"
uuid = "a3789734-cfe1-5b06-b2d0-1dd0d9d62d05"
version = "1.1.3+4"

[[deps.Xorg_libXext_jll]]
deps = ["Artifacts", "JLLWrappers", "Libdl", "Pkg", "Xorg_libX11_jll"]
git-tree-sha1 = "b7c0aa8c376b31e4852b360222848637f481f8c3"
uuid = "1082639a-0dae-5f34-9b06-72781eeb8cb3"
version = "1.3.4+4"

[[deps.Xorg_libXfixes_jll]]
deps = ["Artifacts", "JLLWrappers", "Libdl", "Pkg", "Xorg_libX11_jll"]
git-tree-sha1 = "0e0dc7431e7a0587559f9294aeec269471c991a4"
uuid = "d091e8ba-531a-589c-9de9-94069b037ed8"
version = "5.0.3+4"

[[deps.Xorg_libXi_jll]]
deps = ["Artifacts", "JLLWrappers", "Libdl", "Pkg", "Xorg_libXext_jll", "Xorg_libXfixes_jll"]
git-tree-sha1 = "89b52bc2160aadc84d707093930ef0bffa641246"
uuid = "a51aa0fd-4e3c-5386-b890-e753decda492"
version = "1.7.10+4"

[[deps.Xorg_libXinerama_jll]]
deps = ["Artifacts", "JLLWrappers", "Libdl", "Pkg", "Xorg_libXext_jll"]
git-tree-sha1 = "26be8b1c342929259317d8b9f7b53bf2bb73b123"
uuid = "d1454406-59df-5ea1-beac-c340f2130bc3"
version = "1.1.4+4"

[[deps.Xorg_libXrandr_jll]]
deps = ["Artifacts", "JLLWrappers", "Libdl", "Pkg", "Xorg_libXext_jll", "Xorg_libXrender_jll"]
git-tree-sha1 = "34cea83cb726fb58f325887bf0612c6b3fb17631"
uuid = "ec84b674-ba8e-5d96-8ba1-2a689ba10484"
version = "1.5.2+4"

[[deps.Xorg_libXrender_jll]]
deps = ["Artifacts", "JLLWrappers", "Libdl", "Pkg", "Xorg_libX11_jll"]
git-tree-sha1 = "19560f30fd49f4d4efbe7002a1037f8c43d43b96"
uuid = "ea2f1a96-1ddc-540d-b46f-429655e07cfa"
version = "0.9.10+4"

[[deps.Xorg_libpthread_stubs_jll]]
deps = ["Artifacts", "JLLWrappers", "Libdl", "Pkg"]
git-tree-sha1 = "6783737e45d3c59a4a4c4091f5f88cdcf0908cbb"
uuid = "14d82f49-176c-5ed1-bb49-ad3f5cbd8c74"
version = "0.1.0+3"

[[deps.Xorg_libxcb_jll]]
deps = ["Artifacts", "JLLWrappers", "Libdl", "Pkg", "XSLT_jll", "Xorg_libXau_jll", "Xorg_libXdmcp_jll", "Xorg_libpthread_stubs_jll"]
git-tree-sha1 = "daf17f441228e7a3833846cd048892861cff16d6"
uuid = "c7cfdc94-dc32-55de-ac96-5a1b8d977c5b"
version = "1.13.0+3"

[[deps.Xorg_libxkbfile_jll]]
deps = ["Artifacts", "JLLWrappers", "Libdl", "Pkg", "Xorg_libX11_jll"]
git-tree-sha1 = "926af861744212db0eb001d9e40b5d16292080b2"
uuid = "cc61e674-0454-545c-8b26-ed2c68acab7a"
version = "1.1.0+4"

[[deps.Xorg_xcb_util_image_jll]]
deps = ["Artifacts", "JLLWrappers", "Libdl", "Pkg", "Xorg_xcb_util_jll"]
git-tree-sha1 = "0fab0a40349ba1cba2c1da699243396ff8e94b97"
uuid = "12413925-8142-5f55-bb0e-6d7ca50bb09b"
version = "0.4.0+1"

[[deps.Xorg_xcb_util_jll]]
deps = ["Artifacts", "JLLWrappers", "Libdl", "Pkg", "Xorg_libxcb_jll"]
git-tree-sha1 = "e7fd7b2881fa2eaa72717420894d3938177862d1"
uuid = "2def613f-5ad1-5310-b15b-b15d46f528f5"
version = "0.4.0+1"

[[deps.Xorg_xcb_util_keysyms_jll]]
deps = ["Artifacts", "JLLWrappers", "Libdl", "Pkg", "Xorg_xcb_util_jll"]
git-tree-sha1 = "d1151e2c45a544f32441a567d1690e701ec89b00"
uuid = "975044d2-76e6-5fbe-bf08-97ce7c6574c7"
version = "0.4.0+1"

[[deps.Xorg_xcb_util_renderutil_jll]]
deps = ["Artifacts", "JLLWrappers", "Libdl", "Pkg", "Xorg_xcb_util_jll"]
git-tree-sha1 = "dfd7a8f38d4613b6a575253b3174dd991ca6183e"
uuid = "0d47668e-0667-5a69-a72c-f761630bfb7e"
version = "0.3.9+1"

[[deps.Xorg_xcb_util_wm_jll]]
deps = ["Artifacts", "JLLWrappers", "Libdl", "Pkg", "Xorg_xcb_util_jll"]
git-tree-sha1 = "e78d10aab01a4a154142c5006ed44fd9e8e31b67"
uuid = "c22f9ab0-d5fe-5066-847c-f4bb1cd4e361"
version = "0.4.1+1"

[[deps.Xorg_xkbcomp_jll]]
deps = ["Artifacts", "JLLWrappers", "Libdl", "Pkg", "Xorg_libxkbfile_jll"]
git-tree-sha1 = "4bcbf660f6c2e714f87e960a171b119d06ee163b"
uuid = "35661453-b289-5fab-8a00-3d9160c6a3a4"
version = "1.4.2+4"

[[deps.Xorg_xkeyboard_config_jll]]
deps = ["Artifacts", "JLLWrappers", "Libdl", "Pkg", "Xorg_xkbcomp_jll"]
git-tree-sha1 = "5c8424f8a67c3f2209646d4425f3d415fee5931d"
uuid = "33bec58e-1273-512f-9401-5d533626f822"
version = "2.27.0+4"

[[deps.Xorg_xtrans_jll]]
deps = ["Artifacts", "JLLWrappers", "Libdl", "Pkg"]
git-tree-sha1 = "79c31e7844f6ecf779705fbc12146eb190b7d845"
uuid = "c5fb5394-a638-5e4d-96e5-b29de1b5cf10"
version = "1.4.0+3"

[[deps.Zlib_jll]]
deps = ["Libdl"]
uuid = "83775a58-1f1d-513f-b197-d71354ab007a"
version = "1.2.12+3"

[[deps.Zstd_jll]]
deps = ["Artifacts", "JLLWrappers", "Libdl", "Pkg"]
git-tree-sha1 = "e45044cd873ded54b6a5bac0eb5c971392cf1927"
uuid = "3161d3a3-bdf6-5164-811a-617609db77b4"
version = "1.5.2+0"

[[deps.fzf_jll]]
deps = ["Artifacts", "JLLWrappers", "Libdl", "Pkg"]
git-tree-sha1 = "868e669ccb12ba16eaf50cb2957ee2ff61261c56"
uuid = "214eeab7-80f7-51ab-84ad-2988db7cef09"
version = "0.29.0+0"

[[deps.libaom_jll]]
deps = ["Artifacts", "JLLWrappers", "Libdl", "Pkg"]
git-tree-sha1 = "3a2ea60308f0996d26f1e5354e10c24e9ef905d4"
uuid = "a4ae2306-e953-59d6-aa16-d00cac43593b"
version = "3.4.0+0"

[[deps.libass_jll]]
deps = ["Artifacts", "Bzip2_jll", "FreeType2_jll", "FriBidi_jll", "HarfBuzz_jll", "JLLWrappers", "Libdl", "Pkg", "Zlib_jll"]
git-tree-sha1 = "5982a94fcba20f02f42ace44b9894ee2b140fe47"
uuid = "0ac62f75-1d6f-5e53-bd7c-93b484bb37c0"
version = "0.15.1+0"

[[deps.libblastrampoline_jll]]
deps = ["Artifacts", "Libdl", "OpenBLAS_jll"]
uuid = "8e850b90-86db-534c-a0d3-1478176c7d93"
version = "5.1.1+0"

[[deps.libfdk_aac_jll]]
deps = ["Artifacts", "JLLWrappers", "Libdl", "Pkg"]
git-tree-sha1 = "daacc84a041563f965be61859a36e17c4e4fcd55"
uuid = "f638f0a6-7fb0-5443-88ba-1cc74229b280"
version = "2.0.2+0"

[[deps.libpng_jll]]
deps = ["Artifacts", "JLLWrappers", "Libdl", "Pkg", "Zlib_jll"]
git-tree-sha1 = "94d180a6d2b5e55e447e2d27a29ed04fe79eb30c"
uuid = "b53b4c65-9356-5827-b1ea-8c7a1a84506f"
version = "1.6.38+0"

[[deps.libvorbis_jll]]
deps = ["Artifacts", "JLLWrappers", "Libdl", "Ogg_jll", "Pkg"]
git-tree-sha1 = "b910cb81ef3fe6e78bf6acee440bda86fd6ae00c"
uuid = "f27f6e37-5d2b-51aa-960f-b287f2bc3b7a"
version = "1.3.7+1"

[[deps.nghttp2_jll]]
deps = ["Artifacts", "Libdl"]
uuid = "8e850ede-7688-5339-a07c-302acd2aaf8d"
version = "1.48.0+0"

[[deps.p7zip_jll]]
deps = ["Artifacts", "Libdl"]
uuid = "3f19e933-33d8-53b3-aaab-bd5110c3b7a0"
version = "17.4.0+0"

[[deps.x264_jll]]
deps = ["Artifacts", "JLLWrappers", "Libdl", "Pkg"]
git-tree-sha1 = "4fea590b89e6ec504593146bf8b988b2c00922b2"
uuid = "1270edf5-f2f9-52d2-97e9-ab00b5d0237a"
version = "2021.5.5+0"

[[deps.x265_jll]]
deps = ["Artifacts", "JLLWrappers", "Libdl", "Pkg"]
git-tree-sha1 = "ee567a171cce03570d77ad3a43e90218e38937a9"
uuid = "dfaa095f-4041-5dcd-9319-2fabd8486b76"
version = "3.5.0+0"

[[deps.xkbcommon_jll]]
deps = ["Artifacts", "JLLWrappers", "Libdl", "Pkg", "Wayland_jll", "Wayland_protocols_jll", "Xorg_libxcb_jll", "Xorg_xkeyboard_config_jll"]
git-tree-sha1 = "9ebfc140cc56e8c2156a15ceac2f0302e327ac0a"
uuid = "d8fb68d0-12a3-5cfd-a85a-d49703b185fd"
version = "1.4.1+0"
"""

# ╔═╡ Cell order:
# ╠═d3525d21-d733-4b66-84ad-13fa437dd8bf
# ╠═c39fc80a-44a8-42d8-911c-bf1c937e6bba
# ╠═e9539e47-dc78-43e7-81de-f3e3267ed197
# ╠═b8245233-055a-43b6-8170-70eeccf83495
# ╠═71c1f166-c912-4fea-8d56-84acdc46c083
# ╠═0fe32c74-93b0-11ed-0985-1dfb7d1bb10e
# ╠═56dad226-65bc-4f0b-ab1f-c39c9e7b1270
# ╠═b78fb4bf-c0f2-45b3-88bf-f3eb22094823
# ╠═f1d4ce39-9e80-4042-b6a7-715260da57dc
# ╠═696e90b5-a8c2-4803-9e74-2d29fef911df
# ╠═b55d0ef6-f90d-475a-8097-a71e15064fb7
# ╠═9640b2b8-0d72-458d-9511-b6b419ea80e5
# ╠═b82d0e9b-4615-4107-b719-ff562893f893
# ╠═1ccb54d8-0219-48d9-a282-303f67e646eb
# ╠═70fdd975-62bc-4825-a872-d32b2f924362
# ╠═0a1a8900-0da3-4c2c-849b-b5ebc6d979e2
# ╠═d804f088-e382-4e5d-ae5e-d256142e668e
# ╠═50d0dd29-e890-4144-8427-bceedd404642
# ╠═857ca64f-34cd-461f-8148-b56816232929
# ╠═9bbff24a-623a-403d-85df-109bfebd6c3b
# ╠═c36df7f9-e76a-45d6-aecc-f2c3d2e69ffa
# ╠═38f6fa60-4ce3-4107-9777-ab93d8a104f0
# ╠═df1c4083-065b-4bca-a9a0-f70ed6bf4b52
# ╠═50b358af-6c15-4a2c-a384-8ef0281b5469
# ╠═b6f029a0-8e39-4108-916a-5033b2ade7a2
# ╠═84a67551-9ed1-42be-be5b-cc92acceffe8
# ╠═f44b3e22-6f72-41c0-8c26-1db04f32155d
# ╠═01533808-dad6-4afc-88ae-03bd5402009f
# ╠═62cea919-4d7a-4432-b823-dfe16284fcf6
# ╠═8dafef43-fc69-46c2-8ec0-48c7b839dfcf
# ╠═bdc113bd-9e7f-44e9-b140-61a8f1727b0b
# ╠═34ddf40b-aa55-4441-913e-18956c2b1e93
# ╠═46a4d33b-2ca1-476b-85bf-9f6c4c3a62b7
# ╠═163f44c4-546f-4a29-a028-52d9b4f6be81
# ╠═4bd91592-20a9-4b34-a477-f5143a5e440d
# ╠═9ec03fac-1a30-4093-b480-e5b32e35ab5e
# ╠═2321a3e5-2f23-4478-812e-2f6e2ba28524
# ╠═1f4804ba-fee7-4322-857a-eda7edbd7293
# ╠═983448de-2e7f-46f0-92bc-d1cb30310a73
# ╠═3e607e6f-2b4f-486c-a09b-ae44616e5310
# ╠═1350d262-9ac3-46c4-85b6-b6c3102e36af
# ╠═0182eaeb-953a-4314-9e5d-14be03d2aaa1
# ╠═747a31e0-b161-40bb-9c3b-70b7238fa898
# ╠═eeaf50ba-9f98-4747-afa5-a9ed66bc4d77
# ╠═3d9b7861-5014-49ec-92dc-4784dfde036c
# ╠═1b5c5a4b-a413-4d05-b220-f3e334e0a3c5
# ╠═118e1443-63b3-47d3-aa71-c8ed8a385865
# ╠═b0eec3fe-5a6c-49bb-aed6-6f13e45a68c2
# ╟─00000000-0000-0000-0000-000000000001
# ╟─00000000-0000-0000-0000-000000000002
