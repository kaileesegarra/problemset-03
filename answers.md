# CMPS 6610 Problem Set 03
## Answers

**Name:** Kailee Segarra

Place all written answers from `problemset-03.md` here for easier grading.

**1b.**

The `isearch` algorithm examines each element of the list using `iterate`.

Work:
\[
W(n) = W(n-1) + O(1) = O(n)
\]

Span:
\[
S(n) = S(n-1) + O(1) = O(n)
\]

Therefore, both the work and span are \(O(n)\).

**1d.**

For `rsearch`, the list is reduced by recursively splitting it into two halves.

Work:
\[
W(n) = 2W(n/2) + O(1)
\]

By the Master Theorem:

\[
W(n) = O(n)
\]

Span:
Because the two recursive calls can be done in parallel, only one branch contributes to the critical path:

\[
S(n) = S(n/2) + O(1)
\]

Therefore:

\[
S(n) = O(\log n)
\]

So the resulting algorithm has:

- Work: \(O(n)\)
- Span: \(O(\log n)\)

**1e.**

With `ureduce`, the list is split into parts of size approximately \(n/3\) and \(2n/3\).

Work:

\[
W(n) = W(n/3) + W(2n/3) + O(1)
\]

All elements still have to be processed, so:

\[
W(n) = O(n)
\]

Span:

Since the two recursive calls can be performed in parallel, the span is determined by the larger subproblem:

\[
S(n) = S(2n/3) + O(1)
\]

Therefore:

\[
S(n) = O(\log n)
\]

So the resulting algorithm has:

- Work: \(O(n)\)
- Span: \(O(\log n)\)

**2a.**

A simple way to deduplicate the list while preserving order is to scan the input from left to right and keep track of which elements have already been seen.

    #### SPARC specification

    **S — Specification**

    Input: A list `A` of `n` elements.

    Output: A list containing each distinct element of `A` exactly once, in the same order as its first appearance in `A`.

    **P — Parallelism**

    This algorithm is mostly sequential because whether an element should be included depends on whether it has already appeared earlier in the list.

    **A — Algorithm**

    `dedup(A):`

    - Create an empty set `seen`.
    - Create an empty list `result`.
    - For each element x in A:
    - If x is not in seen:
        - Add x to seen.
        - Append x to result.
    - Return result.

    **R — Recurrence / Runtime**

    Assuming set lookup and insertion take expected \(O(1)\) time, each element is processed once.

    \[
    W(n) = W(n-1) + O(1)
    \]

    Therefore:

    \[
    W(n) = O(n)
    \]

    Because each step depends on the state produced by earlier steps, the span is also:

    \[
    S(n) = S(n-1) + O(1)
    \]

    Therefore:

    \[
    S(n) = O(n)
    \]

    So the algorithm has:

    - Work: \(O(n)\)
    - Span: \(O(n)\)

    **C — Correctness**

    Each element is added to the output only if it has not appeared previously. Therefore, every distinct element appears exactly once. Because the input is processed from left to right, the order of first appearances is preserved.

**2b.**

Since the data is distributed across multiple lists and the order of the unique elements does not matter, the lists can be processed in parallel.

    #### SPARC specification

    **S — Specification**

    Input: A collection of lists \(A_0, A_1, \ldots, A_m\), where each list contains \(n\) elements.

    Output: The distinct elements that occur in any of the input lists. The order of the output elements is not important.

    **P — Parallelism**

    The different input lists can be processed in parallel because identifying unique values does not depend on the order in which the lists are examined.

    Each list can therefore be processed independently, with its elements inserted into a shared set.

    **A — Algorithm**

    `multi-dedup(A):`

    - Create an empty concurrent set `seen`.
    - In parallel, process each list \(A_i\).
    - For each element `x` in \(A_i\), insert `x` into `seen`.
    - After all lists are finished, return the elements in `seen`.

    **R — Recurrence / Runtime**

    There are approximately \(mn\) total elements across all of the lists.

    Assuming expected \(O(1)\) set insertion, the total work is:

    \[
    W(m,n) = O(mn)
    \]

    If the \(m\) lists are processed in parallel, each list requires \(O(n)\) sequential work, so the span is:

    \[
    S(m,n) = O(n)
    \]

    Therefore:

    - Work: \(O(mn)\)
    - Span: \(O(n)\)

    Compared with part 2a, the total work is still linear in the total number of input elements. However, the distributed version allows separate lists to be processed in parallel, so its span does not grow with the number of lists \(m\).

    **C — Correctness**

    Every input element is inserted into the shared set. Since a set stores only one copy of each value, duplicate elements are removed automatically. Therefore, the final set contains exactly the distinct elements that appeared anywhere in the input lists.

**2c.**

Sequence operations can be useful for these deduplication problems, especially `map` and `reduce`.

For the single-list version in part 2a, preserving the order of first appearances makes the problem more sequential. A `map` could be used to process elements, but determining whether an element is a duplicate depends on whether it appeared earlier in the list, so the sequence operations do not remove that dependency very well.

For the distributed version in part 2b, sequence operations are more useful because order does not matter. A `map` operation could process each list independently in parallel, and a `reduce` operation could combine the sets of unique elements produced by the different lists using set union.

For example, each list could first be converted into a set of unique elements, and then those sets could be combined with `reduce` using set union.

This approach has the same overall goal as the shared-set solution but exposes more parallelism because the different lists can be processed independently before their results are combined.


**3b.**

The iterative solution processes the input from left to right using `iterate`.

For the work:

\[
W(n) = W(n-1) + O(1)
\]

Therefore:

\[
W(n) = O(n)
\]

For the span:

\[
S(n) = S(n-1) + O(1)
\]

Therefore:

\[
S(n) = O(n)
\]

So the iterative parenthesis-matching algorithm has:

- Work: \(O(n)\)
- Span: \(O(n)\)

The span is linear because each update depends on the result of the previous step, so the iterations cannot be performed in parallel.

**3d.**

The algorithm first maps each input element to \(1\), \(-1\), or \(0\), then performs a parallel `scan`, and finally uses `reduce` to find the minimum prefix value.

The parallel `map` has:

\[
W_{\text{map}}(n) = O(n)
\]

\[
S_{\text{map}}(n) = O(1)
\]

For the efficient contraction-based `scan`, the work recurrence is:

\[
W_{\text{scan}}(n) = W_{\text{scan}}(n/2) + O(n)
\]

so:

\[
W_{\text{scan}}(n) = O(n)
\]

The span recurrence is:

\[
S_{\text{scan}}(n) = S_{\text{scan}}(n/2) + O(1)
\]

so:

\[
S_{\text{scan}}(n) = O(\log n)
\]

The final `reduce` also has:

\[
W_{\text{reduce}}(n) = O(n)
\]

and

\[
S_{\text{reduce}}(n) = O(\log n)
\]

Therefore, the complete algorithm has:

- Work: \(O(n)\)
- Span: \(O(\log n)\)

**3f.**

The divide-and-conquer algorithm splits the input into two halves, solves both halves recursively, and combines the two results in constant time.

For the work:

\[
W(n) = 2W(n/2) + O(1)
\]

By the Master Theorem:

\[
W(n) = O(n)
\]

For the span, the two recursive calls can be performed in parallel, so only one recursive branch contributes to the critical path:

\[
S(n) = S(n/2) + O(1)
\]

Therefore:

\[
S(n) = O(\log n)
\]

So the divide-and-conquer parenthesis-matching algorithm has:

- Work: \(O(n)\)
- Span: \(O(\log n)\)
