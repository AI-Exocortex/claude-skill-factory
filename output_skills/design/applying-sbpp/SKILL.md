---
name: applying-sbpp
description: Use when designing, implementing, or refactoring Java/Kotlin code to apply Smalltalk Best Practice Patterns (SBPP) adapted for Java 17+ and Kotlin 1.9+.
---

# Applying Smalltalk Best Practice Patterns (SBPP)

STARTER_CHARACTER = 🧶

## Overview

Rigorously apply Kent Beck's Smalltalk Best Practice Patterns (SBPP) to Java and Kotlin code. These patterns focus on communication, consistency, and reducing the gap between code and domain.

**Core Principle:** Code should communicate its intent at a single level of abstraction. If a piece of code needs a comment to explain *what* it does, it needs to be extracted into a method named after its *intent*.

## Pattern Reference Index

| Pattern | Reference Path | When to Use |
| :--- | :--- | :--- |
| **SBPP-BEH-01 - Composed Method** | [reference/ch03_behavior/SBPP-BEH-01_composed_method.md](reference/ch03_behavior/SBPP-BEH-01_composed_method.md) | How do you divide a class's logic into methods so that each method communicates clearly what it does and remains at a single level of abstraction? |
| **SBPP-BEH-02 - Constructor Method** | [reference/ch03_behavior/SBPP-BEH-02_constructor_method.md](reference/ch03_behavior/SBPP-BEH-02_constructor_method.md) | How do you provide object creation in a way that hides internal representation and communicates the intent of each creation scenario? |
| **SBPP-BEH-03 - Constructor Parameter Method** | [reference/ch03_behavior/SBPP-BEH-03_constructor_parameter_method.md](reference/ch03_behavior/SBPP-BEH-03_constructor_parameter_method.md) | How do you initialize instance variables from constructor parameters in a way that keeps the constructor body readable? |
| **SBPP-BEH-04 - Shortcut Constructor Method** | [reference/ch03_behavior/SBPP-BEH-04_shortcut_constructor_method.md](reference/ch03_behavior/SBPP-BEH-04_shortcut_constructor_method.md) | How do you provide a concise creation syntax for objects that are created pervasively, without leaking internal details? |
| **SBPP-BEH-05 - Converter Method** | [reference/ch03_behavior/SBPP-BEH-05_converter_method.md](reference/ch03_behavior/SBPP-BEH-05_converter_method.md) | How do you represent the conversion of an object into another object with compatible state but different protocols? |
| **SBPP-BEH-06 - Converter Constructor Method** | [reference/ch03_behavior/SBPP-BEH-06_converter_constructor_method.md](reference/ch03_behavior/SBPP-BEH-06_converter_constructor_method.md) | How do you convert an object of one type into an object of a substantially different type while maintaining clear intent? |
| **SBPP-BEH-07 - Query Method** | [reference/ch03_behavior/SBPP-BEH-07_query_method.md](reference/ch03_behavior/SBPP-BEH-07_query_method.md) | How do you represent testing a property of an object so that callers can write self-documenting code? |
| **SBPP-BEH-08 - Comparing Method** | [reference/ch03_behavior/SBPP-BEH-08_comparing_method.md](reference/ch03_behavior/SBPP-BEH-08_comparing_method.md) | How do you provide natural ordering for an object when there is one clear, dominant way to compare instances? |
| **SBPP-BEH-09 - Reversing Method** | [reference/ch03_behavior/SBPP-BEH-09_reversing_method.md](reference/ch03_behavior/SBPP-BEH-09_reversing_method.md) | How do you rewrite code that passes objects as arguments to restore the "single receiver" focus? |
| **SBPP-BEH-10 - Method Object** | [reference/ch03_behavior/SBPP-BEH-10_method_object.md](reference/ch03_behavior/SBPP-BEH-10_method_object.md) | How do you organise a method whose complexity cannot be reduced by Composed Method because it needs its own state? |
| **SBPP-BEH-11 - Execute Around Method** | [reference/ch03_behavior/SBPP-BEH-11_execute_around_method.md](reference/ch03_behavior/SBPP-BEH-11_execute_around_method.md) | How do you ensure that a pair of operations (setup + teardown) is always executed correctly using lambdas? |
| **SBPP-BEH-12 - Debug Printing Method** | [reference/ch03_behavior/SBPP-BEH-12_debug_printing_method.md](reference/ch03_behavior/SBPP-BEH-12_debug_printing_method.md) | How do you implement toString() so that it provides maximum debugging utility for developers? |
| **SBPP-BEH-13 - Method Comment** | [reference/ch03_behavior/SBPP-BEH-13_method_comment.md](reference/ch03_behavior/SBPP-BEH-13_method_comment.md) | How do you comment methods so that comments add genuine value instead of repeating what the code says? |
| **SBPP-BEH-14 - Message** | [reference/ch03_behavior/SBPP-BEH-14_message.md](reference/ch03_behavior/SBPP-BEH-14_message.md) | How do you invoke computation in an object-oriented system so that the receiver has the final say? |
| **SBPP-BEH-15 - Choosing Message** | [reference/ch03_behavior/SBPP-BEH-15_choosing_message.md](reference/ch03_behavior/SBPP-BEH-15_choosing_message.md) | How do you execute one of several alternative behaviours based on runtime type using polymorphism instead of conditionals? |
| **SBPP-BEH-16 - Decomposing Message** | [reference/ch03_behavior/SBPP-BEH-16_decomposing_message.md](reference/ch03_behavior/SBPP-BEH-16_decomposing_message.md) | How do you break a computation into named parts that can be understood independently? |
| **SBPP-BEH-17 - Intention Revealing Message** | [reference/ch03_behavior/SBPP-BEH-17_intention_revealing_message.md](reference/ch03_behavior/SBPP-BEH-17_intention_revealing_message.md) | How do you communicate the intent of a simple operation when the implementation alone is obscure? |
| **SBPP-BEH-18 - Intention Revealing Selector** | [reference/ch03_behavior/SBPP-BEH-18_intention_revealing_selector.md](reference/ch03_behavior/SBPP-BEH-18_intention_revealing_selector.md) | What do you name a method so that its purpose is immediately clear from the name alone? |
| **SBPP-BEH-19 - Dispatched Interpretation** | [reference/ch03_behavior/SBPP-BEH-19_dispatched_interpretation.md](reference/ch03_behavior/SBPP-BEH-19_dispatched_interpretation.md) | How can two objects cooperate when one wishes to perform an operation on data whose structure it doesn't know? |
| **SBPP-BEH-20 - Double Dispatch** | [reference/ch03_behavior/SBPP-BEH-20_double_dispatch.md](reference/ch03_behavior/SBPP-BEH-20_double_dispatch.md) | How do you implement a computation whose logic depends on the runtime types of two collaborating objects? |
| **SBPP-BEH-21 - Mediating Protocol** | [reference/ch03_behavior/SBPP-BEH-21_mediating_protocol.md](reference/ch03_behavior/SBPP-BEH-21_mediating_protocol.md) | How do you formalise the interaction protocol between two independent objects without creating tight coupling? |
| **SBPP-BEH-22 - Super** | [reference/ch03_behavior/SBPP-BEH-22_super.md](reference/ch03_behavior/SBPP-BEH-22_super.md) | How do you invoke superclass behaviour when a subclass needs to build on or extend existing functionality? |
| **SBPP-BEH-23 - Extending Super** | [reference/ch03_behavior/SBPP-BEH-23_extending_super.md](reference/ch03_behavior/SBPP-BEH-23_extending_super.md) | How do you add behaviour to a superclass method in a subclass without duplicating the superclass's logic? |
| **SBPP-BEH-24 - Modifying Super** | [reference/ch03_behavior/SBPP-BEH-24_modifying_super.md](reference/ch03_behavior/SBPP-BEH-24_modifying_super.md) | How do you change part of a superclass method's behaviour in a subclass when the change is local? |
| **SBPP-BEH-25 - Delegation** | [reference/ch03_behavior/SBPP-BEH-25_delegation.md](reference/ch03_behavior/SBPP-BEH-25_delegation.md) | How does an object share implementation with another object when inheritance is inappropriate? |
| **SBPP-BEH-26 - Simple Delegation** | [reference/ch03_behavior/SBPP-BEH-26_simple_delegation.md](reference/ch03_behavior/SBPP-BEH-26_simple_delegation.md) | How do you invoke a disinterested delegate that needs no reference back to the delegating object? |
| **SBPP-BEH-27 - Self Delegation** | [reference/ch03_behavior/SBPP-BEH-27_self_delegation.md](reference/ch03_behavior/SBPP-BEH-27_self_delegation.md) | How do you implement delegation to a collaborator that needs a reference back to the delegating object? |
| **SBPP-BEH-28 - Pluggable Behavior** | [reference/ch03_behavior/SBPP-BEH-28_pluggable_behavior.md](reference/ch03_behavior/SBPP-BEH-28_pluggable_behavior.md) | How do you allow an object's behaviour to vary at runtime without creating a subclass explosion? |
| **SBPP-BEH-29 - Pluggable Selector** | [reference/ch03_behavior/SBPP-BEH-29_pluggable_selector.md](reference/ch03_behavior/SBPP-BEH-29_pluggable_selector.md) | How do you implement simple pluggable behaviour where the varying part is a method call? |
| **SBPP-BEH-30 - Pluggable Block** | [reference/ch03_behavior/SBPP-BEH-30_pluggable_block.md](reference/ch03_behavior/SBPP-BEH-30_pluggable_block.md) | How do you plug in complex behaviour that is not implemented as a method on an existing object? |
| **SBPP-BEH-31 - Collecting Parameter** | [reference/ch03_behavior/SBPP-BEH-31_collecting_parameter.md](reference/ch03_behavior/SBPP-BEH-31_collecting_parameter.md) | How do you accumulate results from several methods that collaborate on building a collection? |
| **SBPP-CLS-01 - Simple Superclass Name** | [reference/ch06_classes/SBPP-CLS-01_simple_superclass_name.md](reference/ch06_classes/SBPP-CLS-01_simple_superclass_name.md) | What do you name a class that is the root of a hierarchy to communicate its essence? |
| **SBPP-CLS-02 - Qualified Subclass Name** | [reference/ch06_classes/SBPP-CLS-02_qualified_subclass_name.md](reference/ch06_classes/SBPP-CLS-02_qualified_subclass_name.md) | What do you name a subclass so that readers understand how it differs from its superclass? |
| **SBPP-COL-01 - Collection** | [reference/ch05_collections/SBPP-COL-01_collection.md](reference/ch05_collections/SBPP-COL-01_collection.md) | How do you represent a one-to-many relationship choosing the right collection abstraction? |
| **SBPP-COL-02 - OrderedCollection** | [reference/ch05_collections/SBPP-COL-02_orderedcollection.md](reference/ch05_collections/SBPP-COL-02_orderedcollection.md) | How do you represent a collection whose size varies at runtime without arbitrary constraints? |
| **SBPP-COL-03 - RunArray** | [reference/ch05_collections/SBPP-COL-03_runarray.md](reference/ch05_collections/SBPP-COL-03_runarray.md) | How do you compactly represent a collection where the same element repeats many times in a row? |
| **SBPP-COL-04 - Set** | [reference/ch05_collections/SBPP-COL-04_set.md](reference/ch05_collections/SBPP-COL-04_set.md) | How do you represent a collection whose elements must be unique? |
| **SBPP-COL-05 - Equality Method** | [reference/ch05_collections/SBPP-COL-05_equality_method.md](reference/ch05_collections/SBPP-COL-05_equality_method.md) | How do you define equality for a new class so that instances with the same state are equal? |
| **SBPP-COL-06 - Hashing Method** | [reference/ch05_collections/SBPP-COL-06_hashing_method.md](reference/ch05_collections/SBPP-COL-06_hashing_method.md) | How do you implement hashCode() correctly so that objects work reliably in hash-based collections? |
| **SBPP-COL-07 - Dictionary** | [reference/ch05_collections/SBPP-COL-07_dictionary.md](reference/ch05_collections/SBPP-COL-07_dictionary.md) | How do you map one kind of object to another for efficient retrieval? |
| **SBPP-COL-08 - SortedCollection** | [reference/ch05_collections/SBPP-COL-08_sortedcollection.md](reference/ch05_collections/SBPP-COL-08_sortedcollection.md) | How do you maintain a collection in sorted order so elements are always accessible? |
| **SBPP-COL-09 - Array** | [reference/ch05_collections/SBPP-COL-09_array.md](reference/ch05_collections/SBPP-COL-09_array.md) | How do you represent a collection with a fixed number of elements? |
| **SBPP-COL-10 - ByteArray** | [reference/ch05_collections/SBPP-COL-10_bytearray.md](reference/ch05_collections/SBPP-COL-10_bytearray.md) | How do you represent and work with binary data (byte sequences) efficiently? |
| **SBPP-COL-11 - Interval** | [reference/ch05_collections/SBPP-COL-11_interval.md](reference/ch05_collections/SBPP-COL-11_interval.md) | How do you represent a sequence of consecutive numbers without allocating memory for each? |
| **SBPP-COL-12 - IsEmpty** | [reference/ch05_collections/SBPP-COL-12_isempty.md](reference/ch05_collections/SBPP-COL-12_isempty.md) | How do you test whether a collection is empty in a way that communicates intent clearly? |
| **SBPP-COL-13 - Includes** | [reference/ch05_collections/SBPP-COL-13_includes.md](reference/ch05_collections/SBPP-COL-13_includes.md) | How do you test whether a specific element is present in a collection? |
| **SBPP-COL-14 - Concatenation** | [reference/ch05_collections/SBPP-COL-14_concatenation.md](reference/ch05_collections/SBPP-COL-14_concatenation.md) | How do you combine multiple collections into one without unnecessary copies? |
| **SBPP-COL-15 - Enumeration** | [reference/ch05_collections/SBPP-COL-15_enumeration.md](reference/ch05_collections/SBPP-COL-15_enumeration.md) | How do you express code that applies an operation to every element of a collection? |
| **SBPP-COL-16 - Do** | [reference/ch05_collections/SBPP-COL-16_do.md](reference/ch05_collections/SBPP-COL-16_do.md) | How do you execute a block of code for each element in a collection? |
| **SBPP-COL-17 - Collect** | [reference/ch05_collections/SBPP-COL-17_collect.md](reference/ch05_collections/SBPP-COL-17_collect.md) | How do you produce a new collection by applying a function to each element? |
| **SBPP-COL-18 - Select/Reject** | [reference/ch05_collections/SBPP-COL-18_select_reject.md](reference/ch05_collections/SBPP-COL-18_select_reject.md) | How do you produce a sub-collection of elements that meet or fail a criterion? |
| **SBPP-COL-19 - Detect** | [reference/ch05_collections/SBPP-COL-19_detect.md](reference/ch05_collections/SBPP-COL-19_detect.md) | How do you find the first element in a collection that meets a criterion? |
| **SBPP-COL-20 - Inject:into (Reduce/Fold)** | [reference/ch05_collections/SBPP-COL-20_inject_into.md](reference/ch05_collections/SBPP-COL-20_inject_into.md) | How do you reduce a collection to a single value by applying a combining function? |
| **SBPP-COL-21 - Duplicate Removing Set** | [reference/ch05_collections/SBPP-COL-21_duplicate_removing_set.md](reference/ch05_collections/SBPP-COL-21_duplicate_removing_set.md) | How do you remove duplicate elements from a collection efficiently? |
| **SBPP-COL-22 - Temporarily Sorted Collection** | [reference/ch05_collections/SBPP-COL-22_temporarily_sorted_collection.md](reference/ch05_collections/SBPP-COL-22_temporarily_sorted_collection.md) | How do you sort a collection for one specific use case without paying long-term sorting costs? |
| **SBPP-COL-23 - Stack** | [reference/ch05_collections/SBPP-COL-23_stack.md](reference/ch05_collections/SBPP-COL-23_stack.md) | How do you implement LIFO (Last-In, First-Out) stack semantics? |
| **SBPP-COL-24 - Queue** | [reference/ch05_collections/SBPP-COL-24_queue.md](reference/ch05_collections/SBPP-COL-24_queue.md) | How do you implement FIFO (First-In, First-Out) queue semantics? |
| **SBPP-COL-25 - Searching Literal** | [reference/ch05_collections/SBPP-COL-25_searching_literal.md](reference/ch05_collections/SBPP-COL-25_searching_literal.md) | How do you test whether a value is one of a small fixed set of known literals efficiently? |
| **SBPP-COL-26 - Lookup Cache** | [reference/ch05_collections/SBPP-COL-26_lookup_cache.md](reference/ch05_collections/SBPP-COL-26_lookup_cache.md) | How do you optimise repeated searches against a collection by a specific attribute? |
| **SBPP-COL-27 - Parsing Stream** | [reference/ch05_collections/SBPP-COL-27_parsing_stream.md](reference/ch05_collections/SBPP-COL-27_parsing_stream.md) | How do you write a simple parser that reads tokens or lines sequentially? |
| **SBPP-COL-28 - Concatenating Stream** | [reference/ch05_collections/SBPP-COL-28_concatenating_stream.md](reference/ch05_collections/SBPP-COL-28_concatenating_stream.md) | How do you concatenate many string pieces or collections efficiently? |
| **SBPP-FMT-01 - Inline Message Pattern** | [reference/ch07_formatting/SBPP-FMT-01_inline_message_pattern.md](reference/ch07_formatting/SBPP-FMT-01_inline_message_pattern.md) | How do you format a method signature so that it is readable at a glance? |
| **SBPP-FMT-02 - Type Suggesting Parameter Name** | [reference/ch07_formatting/SBPP-FMT-02_type_suggesting_parameter_name.md](reference/ch07_formatting/SBPP-FMT-02_type_suggesting_parameter_name.md) | What do you name method parameters so that their purpose at the call site is clear? |
| **SBPP-FMT-03 - Indented Control Flow** | [reference/ch07_formatting/SBPP-FMT-03_indented_control_flow.md](reference/ch07_formatting/SBPP-FMT-03_indented_control_flow.md) | How do you format multi-part expressions and nested blocks for clarity? |
| **SBPP-FMT-04 - Rectangular Block** | [reference/ch07_formatting/SBPP-FMT-04_rectangular_block.md](reference/ch07_formatting/SBPP-FMT-04_rectangular_block.md) | How do you format lambda bodies and anonymous blocks for immediate recognition? |
| **SBPP-FMT-05 - Guard Clause** | [reference/ch07_formatting/SBPP-FMT-05_guard_clause.md](reference/ch07_formatting/SBPP-FMT-05_guard_clause.md) | How do you format methods handling invalid cases first with early returns? |
| **SBPP-FMT-06 - Conditional Expression** | [reference/ch07_formatting/SBPP-FMT-06_conditional_expression.md](reference/ch07_formatting/SBPP-FMT-06_conditional_expression.md) | How do you format conditionals where both branches produce the same kind of result? |
| **SBPP-FMT-07 - Simple Enumeration Parameter** | [reference/ch07_formatting/SBPP-FMT-07_simple_enumeration_parameter.md](reference/ch07_formatting/SBPP-FMT-07_simple_enumeration_parameter.md) | What do you name the iteration variable inside a lambda to communicate its role? |
| **SBPP-FMT-08 - Cascade** | [reference/ch07_formatting/SBPP-FMT-08_cascade.md](reference/ch07_formatting/SBPP-FMT-08_cascade.md) | How do you express multiple operations on the same object concisely? |
| **SBPP-FMT-09 - Yourself** | [reference/ch07_formatting/SBPP-FMT-09_yourself.md](reference/ch07_formatting/SBPP-FMT-09_yourself.md) | How do you ensure that a multi-message sequence returns the original receiver object? |
| **SBPP-FMT-10 - Interesting Return Value** | [reference/ch07_formatting/SBPP-FMT-10_interesting_return_value.md](reference/ch07_formatting/SBPP-FMT-10_interesting_return_value.md) | When should a method explicitly return a value versus returning nothing? |
| **SBPP-STA-01 - Common State** | [reference/ch04_state/SBPP-STA-01_common_state.md](reference/ch04_state/SBPP-STA-01_common_state.md) | How do you represent state shared by all instances of a class explicitly? |
| **SBPP-STA-02 - Variable State** | [reference/ch04_state/SBPP-STA-02_variable_state.md](reference/ch04_state/SBPP-STA-02_variable_state.md) | How do you represent state that only some instances of a class have? |
| **SBPP-STA-03 - Explicit Initialization** | [reference/ch04_state/SBPP-STA-03_explicit_initialization.md](reference/ch04_state/SBPP-STA-03_explicit_initialization.md) | How do you initialize an instance variable to its default value clearly and deterministically? |
| **SBPP-STA-04 - Lazy Initialization** | [reference/ch04_state/SBPP-STA-04_lazy_initialization.md](reference/ch04_state/SBPP-STA-04_lazy_initialization.md) | How do you initialize an instance variable only when it is first needed? |
| **SBPP-STA-05 - Default Value Method** | [reference/ch04_state/SBPP-STA-05_default_value_method.md](reference/ch04_state/SBPP-STA-05_default_value_method.md) | How do you represent a default value for a variable when the default is complex? |
| **SBPP-STA-06 - Constant Method** | [reference/ch04_state/SBPP-STA-06_constant_method.md](reference/ch04_state/SBPP-STA-06_constant_method.md) | How do you represent a constant value that does not change between instances? |
| **SBPP-STA-07 - Direct Variable Access** | [reference/ch04_state/SBPP-STA-07_direct_variable_access.md](reference/ch04_state/SBPP-STA-07_direct_variable_access.md) | How do you access instance variables within a class directly for readability? |
| **SBPP-STA-08 - Indirect Variable Access** | [reference/ch04_state/SBPP-STA-08_indirect_variable_access.md](reference/ch04_state/SBPP-STA-08_indirect_variable_access.md) | How do you access instance variables within a class using accessors for flexibility? |
| **SBPP-STA-09 - Getting Method** | [reference/ch04_state/SBPP-STA-09_getting_method.md](reference/ch04_state/SBPP-STA-09_getting_method.md) | How do you provide access to an instance variable while encapsulating storage? |
| **SBPP-STA-10 - Setting Method** | [reference/ch04_state/SBPP-STA-10_setting_method.md](reference/ch04_state/SBPP-STA-10_setting_method.md) | How do you allow controlled modification of an instance variable? |
| **SBPP-STA-11 - Collection Accessor Method** | [reference/ch04_state/SBPP-STA-11_collection_accessor_method.md](reference/ch04_state/SBPP-STA-11_collection_accessor_method.md) | How do you provide safe, controlled access to an internal collection? |
| **SBPP-STA-12 - Enumeration Method** | [reference/ch04_state/SBPP-STA-12_enumeration_method.md](reference/ch04_state/SBPP-STA-12_enumeration_method.md) | How do you provide safe iteration over a private collection using lambdas? |
| **SBPP-STA-13 - Boolean Property Setting Method** | [reference/ch04_state/SBPP-STA-13_boolean_property_setting_method.md](reference/ch04_state/SBPP-STA-13_boolean_property_setting_method.md) | How do you provide a way to set a boolean property with clear intent? |
| **SBPP-STA-14 - Role Suggesting Instance Variable Name** | [reference/ch04_state/SBPP-STA-14_role_suggesting_instance_variable_name.md](reference/ch04_state/SBPP-STA-14_role_suggesting_instance_variable_name.md) | What do you name an instance variable to communicate its domain role instantly? |
| **SBPP-STA-15 - Temporary Variable** | [reference/ch04_state/SBPP-STA-15_temporary_variable.md](reference/ch04_state/SBPP-STA-15_temporary_variable.md) | How do you use local variables within a method to communicate intent? |
| **SBPP-STA-16 - Collecting Temporary Variable** | [reference/ch04_state/SBPP-STA-16_collecting_temporary_variable.md](reference/ch04_state/SBPP-STA-16_collecting_temporary_variable.md) | How do you gradually accumulate intermediate results within a method body? |
| **SBPP-STA-17 - Caching Temporary Variable** | [reference/ch04_state/SBPP-STA-17_caching_temporary_variable.md](reference/ch04_state/SBPP-STA-17_caching_temporary_variable.md) | How do you avoid recomputing an expensive expression within a method? |
| **SBPP-STA-18 - Explaining Temporary Variable** | [reference/ch04_state/SBPP-STA-18_explaining_temporary_variable.md](reference/ch04_state/SBPP-STA-18_explaining_temporary_variable.md) | How do you simplify a complex expression by naming its parts with local variables? |
| **SBPP-STA-19 - Reusing Temporary Variable** | [reference/ch04_state/SBPP-STA-19_reusing_temporary_variable.md](reference/ch04_state/SBPP-STA-19_reusing_temporary_variable.md) | How do you use an expression several times within a method without recomputing it? |
| **SBPP-STA-20 - Role Suggesting Temporary Variable Name** | [reference/ch04_state/SBPP-STA-20_role_suggesting_temporary_variable_name.md](reference/ch04_state/SBPP-STA-20_role_suggesting_temporary_variable_name.md) | What do you name a local variable so its role in the computation is clear? |

## Rigorous Application Rules

### 1. Composed Method (SBPP-BEH-01)
- Every method SHALL contain statements at only ONE level of abstraction.
- A method body should read like a table of contents — each line names a step, none of the lines implements one.
- Extract any sub-operation that can be named meaningfully into its own private method.

### 2. Constructor Parameter Method (SBPP-BEH-03)
- Do NOT bloat constructors with validation or transformation logic.
- Delegate parameter initialization to named private methods (e.g., `validateFactors()`, `resolveBaseRate()`).
- Call these methods directly in the constructor assignment.

### 3. Intention Revealing Selector (SBPP-BEH-18)
- Name methods after *what* they accomplish (intent), not *how* they work (implementation).
- Avoid generic names like `process()`, `handle()`, `execute()` unless they are the root of a command hierarchy.
- Use domain vocabulary recognizable to non-developers.

### 4. Role Suggesting Names (SBPP-STA-14/20)
- Name fields and local variables after their domain role, not their type.
- ❌ Avoid: `repository`, `itemList`, `amountDouble`.
- ✅ Use: `orderRepository`, `coverageItems`, `basePremium`.

### 5. Modern Adaptations
- **Value Objects:** Use Java `record` (Java 16+) or Kotlin `data class`.
- **Collections:** Use interface-typed fields (`List`, `Set`, `Map`) and return immutable views.
- **Control Flow:** Use Guard Clauses (SBPP-FMT-05) to flatten nesting. Prefer `require`/`check` in Kotlin.
- **Iteration:** Prefer functional pipelines (`map`, `filter`, `fold`) over imperative loops.

## Common Mistakes to Refuse

| Excuse / Anti-Pattern | Reality / SBPP Fix |
|-----------------------|--------------------|
| "It's just a small validation" | Inline logic bloats constructors. Use Constructor Parameter Method. |
| "Persist and notify are one step" | They are different abstraction levels. Separate them in a Composed Method. |
| "repo is shorter than orderRepository" | Brevity is not communication. Use Role Suggesting Names. |
| "I'll add a comment to explain this loop" | Comments reveal missing extractions. Use Composed Method + Intention Revealing Selector. |
| "Nested if is clear enough" | Deep nesting hides the happy path. Use Guard Clauses. |
