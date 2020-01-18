# bluebin
Markdown with reusable components!

## Goal
Bluebin markdown flavour that features reusable components that make complex designs easier. Bluebin projects are meant to be rendered, but should still be legible in their original form.

## The Basics
Most basic markdown is valid in bluebin. This includes headers, lists, emphasis, links, images, and code. See the [original spec](https://daringfireball.net/projects/markdown/basics) for more info.

### Defining components
Let's start by defining a component.

	[my component]
	my property: recycling
	my other property: rules
	
	# %my property%
	*%my other property%*

Here, `[my component]` says that we are defining a component named "my component". My component has two properties: `my property` and `my other property`. An empty line signifies the end of the component header. Everything after this is the component content. Here, you can use all regular markdown expressions with the addition of % substitutions. `%my property%` and `%my other property%` say to replace these with the values of `my property` and `my other property`.

That's it!
