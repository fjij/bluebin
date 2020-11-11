# bluebin
Markdown with reusable components!

## Goal
Bluebin markdown flavour that features reusable components that make complex designs easier. Bluebin projects are meant to be rendered, but should still be legible in their original form.

## Usage
	python3 bluebin.py input_file.bb output_file.md

## The Basics
Most basic markdown is valid in Bluebin. This includes headers, lists, emphasis, links, images, and code. See the [original spec](https://daringfireball.net/projects/markdown/basics) for more info.

### Defining components
Let's start by defining a component.

	[my component]
	my property: recycling
	my other property: rules
	
	# %my property%
	*% my property %* **%my other property%**

#### The header
Here, `[my component]` s that we are defining a component named "my component".
We give our component two **case-senstive** properties: `my property` and `my other property`.
An empty line signifies the end of the component header.

#### Content
Everything after this is the component content. Here, you can use all regular markdown expressions with the addition of % substitutions. `%my property%` and `%my other property%` say to replace these with the values of `my property` and `my other property`.

You don't have to mark the end of a component.

That's it. Our component represents the following markdown:

	# recycling
	*recylcing* **rules**

### Reusing components
So far, we have just defined a more complicated way to do the same thing. The power in components is your ability to reuse them in multiple places, even within other components. There are multiple ways to reuse a component:

	%[my component]
	
	%[my component](bluebin)
	
	%[my component](food, tastes good)
	
	%[my component](", _ ,", ":)")
	
	%[my component](my other property: is awesome)

Reusing a component allows you to use the same content in multiple places. You can also overwrite some of the property values implicitly (order matters) or explicitly (you must state their names). You may use double-quotes if needed. You can even use other properties here! The above bluebin code converts to the following markdown:

	# recycling
	*recylcing* **rules**
	
	# bluebin
	*bluebin* **rules**
	
	# food
	*food* **tastes good**
	
	# , _ ,
	*, _ ,* **:)**
	
	# recycling
	*recylcing* **is awesome**

### Default components and component order
If your bluebin file only contains components, the first component will be displayed by default. If there is markdown before the first component, this markdown will be displayed instead. Best practice is to only reuse components that have been defined **below** the current line, though it is not required. Reusing a component within itself is undefined behavior and results will depend on the implementation.
