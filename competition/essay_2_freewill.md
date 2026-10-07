# Formalizing 'Could Have Done Otherwise': A Structural Defense of Compatibilist Free Will

**Abstract**
The debate over free will and determinism frequently stalls on the ambiguous semantics of the phrase "could have done otherwise." Incompatibilists argue that in a deterministic universe, alternate possibilities are physically closed, rendering moral responsibility null. Compatibilists argue that "could have done otherwise" refers to a hypothetical capacity (e.g., "would have done otherwise if I had desired to"), which incompatibilists often reject as a linguistic sleight of hand. This essay proposes a novel, mathematically rigorous defense of compatibilist free will by grounding the concept in Judea Pearl’s Structural Causal Models (SCMs). I argue that "free will" is not a violation of physical laws, but a property of *Structural Sensitivity* within a causal graph. By formalizing the Principle of Alternate Possibilities through Pearl’s $do$-calculus, I demonstrate that applying a counterfactual intervention—$do(\text{Action})$—meaningfully alters the probability distribution of the Moral Consequence node. Furthermore, I argue that the capacity to internally calculate this Counterfactual Regret is the exact physical and computational mechanism of moral agency. In this framework, determinism does not negate free will; rather, deterministic causal structures provide the necessary scaffolding for counterfactual reasoning and moral responsibility.

### 1. Introduction
The philosophical battleground between compatibilism and incompatibilism is one of the most enduring in the history of ideas. At its core, the conflict centers on the compatibility of determinism—the thesis that every event is necessitated by antecedent events and conditions together with the laws of nature—and the kind of free will required for moral responsibility. The incompatibilist intuition is powerfully formalized in Peter van Inwagen’s Consequence Argument: if determinism is true, then our acts are the consequences of the laws of nature and events in the remote past. But it is not up to us what went on before we were born, and neither is it up to us what the laws of nature are. Therefore, the consequences of these things (including our present acts) are not up to us. 

Central to this debate is the Principle of Alternate Possibilities (PAP), which states that a person is morally responsible for what they have done only if they could have done otherwise. If the universe is deterministic, the incompatibilist argues, there is exactly one physically possible future. Thus, no one "could have done otherwise" in any deep, metaphysical sense. 

Historically, compatibilists have responded by analyzing "could have done otherwise" conditionally. Classical compatibilists like G.E. Moore argued that it simply means "would have done otherwise *if* the agent had chosen to do so." Incompatibilists rightly criticize this as evasive. It changes the subject from the categorical reality of the agent’s constraints to a hypothetical scenario that, ex hypothesi, could never occur.

This essay seeks to rescue compatibilism from the charge of linguistic evasion by providing a formal, structural definition of "could have done otherwise." Drawing upon the revolutionary work of Judea Pearl in causal inference and Structural Causal Models (SCMs), I propose that the compatibilist intuition is not only defensible but mathematically formalizable. Free will, I argue, should not be understood as indeterminism or a "ghost in the machine," but as *Structural Sensitivity*. A system possesses moral agency if it contains an internal architecture capable of representing causal graphs and computing counterfactual interventions via the $do$-operator. In this framework, moral responsibility is justified not by the agent's ability to break physics, but by the agent's structural locus as a node that calculates and is sensitive to Counterfactual Regret.

### 2. The Ambiguity of "Could Have Done Otherwise"
Before introducing the formal machinery of SCMs, it is necessary to diagnose why the traditional debate remains intractable. The phrase "could have done otherwise" suffers from severe semantic overload.

When a physicist states that a particle "could not have taken a different path," they are making a claim about the nomological necessity of the universe’s time-evolution. Given state $S_t$ at time $t$ and laws $L$, state $S_{t+1}$ is uniquely determined. Let us call this *Metaphysical Openness*. If determinism holds, Metaphysical Openness is strictly zero.

However, when an engineer says, "This thermostat could have turned off the furnace, but it was broken," they are not violating determinism. They are describing the functional capacity of a system. The thermostat’s failure to turn off the furnace was deterministically necessitated by a broken wire, but the *type* of mechanism the thermostat is—a temperature-regulating control system—possesses a structural mapping between temperature inputs and electrical outputs. The engineer is pointing out that under a different configuration of the local causal graph (i.e., a fixed wire), the output would vary. Let us call this *Structural Sensitivity*.

The incompatibilist insists that moral responsibility requires Metaphysical Openness. The compatibilist insists that it only requires a highly sophisticated form of Structural Sensitivity. The challenge for the compatibilist has always been to prove that Structural Sensitivity is a robust enough concept to support the weight of moral blame and praise, without collapsing into the trivial sense in which a thermostat "decides" to turn on the heat. To do this, we need a mathematical language of causation that distinguishes between mere correlation, physical mechanism, and counterfactual reasoning.

### 3. Structural Causal Models: A Primer
Judea Pearl’s Structural Causal Models provide the exact epistemology required to formalize Structural Sensitivity. An SCM is defined as a tuple $M = \langle U, V, F, P(u) \rangle$:
- $U$ is a set of exogenous (unobserved, background) variables, determined outside the model.
- $V$ is a set of endogenous (observed) variables.
- $F$ is a set of structural equations $\{f_1, f_2, ..., f_n\}$, where each $f_i$ is a function that determines the value of $V_i \in V$ based on the values of a subset of other variables in $U \cup V$. These are the causal mechanisms.
- $P(u)$ is a probability distribution over the exogenous variables.

Crucially, Pearl defines a "Ladder of Causation" consisting of three levels of cognitive abstraction:
1. **Association (Seeing):** $P(y|x)$. What is the probability of $Y$ given that we observe $X$? This is the domain of standard statistics and machine learning.
2. **Intervention (Doing):** $P(y|do(x))$. What is the probability of $Y$ if we forcibly set the value of $X$ to $x$, cutting off $X$ from its usual causal parents? This is the domain of experimental design and causal graphs.
3. **Counterfactuals (Imagining):** $P(y_{x'}|x, y)$. Given that we observed $X=x$ and $Y=y$, what would $Y$ have been if we had set $X=x'$? This requires a fully specified structural model to simulate alternate realities based on actualized exogenous conditions.

A purely deterministic universe can be modeled as an SCM where $P(u)$ assigns a probability of 1 to a specific background state, and the equations $F$ are deterministic. In such a model, every variable $V_i$ has exactly one realized value. However—and this is the critical insight—the *structural equations $F$ remain intact*. The edges of the causal graph do not vanish just because the inputs are fixed. The relationships defining *how* variables depend on one another transcend the specific instantiation of the universe.

### 4. Determinism and the Structural Graph
Let us construct a simplified SCM of a moral decision. 
- $U_{bg}$: The agent’s genetic predispositions and childhood environment (exogenous).
- $B$: The agent’s current brain state, beliefs, and desires (endogenous).
- $A$: The action the agent takes (e.g., stealing a loaf of bread).
- $C$: The consequence of the action (e.g., the baker starves, the agent is fed).

The structural equations might be:
$B = f_B(U_{bg})$
$A = f_A(B)$
$C = f_C(A, U_{env})$

In a deterministic universe, given a specific $U_{bg}$, the values $B=b$, $A=a$, and $C=c$ are all logically necessitated. The incompatibilist looks at this graph, sees the unbroken chain of necessity from $U_{bg}$ to $C$, and concludes that the agent $A$ is a mere conduit. Because $A=a$ is necessitated by $U_{bg}$, the agent "could not have done otherwise."

This view conflates the *value* of the node with the *function* of the node. The node $A$ is not merely a scalar value $a$; it represents the structural mechanism $f_A(B)$. To understand what "could have done otherwise" means, we must move from the first level of Pearl’s ladder (observation of the actual state) to the second and third levels (intervention and counterfactuals).

### 5. Formalizing the Alternate Possibility via the $do$-Calculus
When we ask, "Could the agent have done otherwise?", we are not asking, "Given $U_{bg}$, is it mathematically possible for $f_A(f_B(U_{bg}))$ to evaluate to something other than $a$?" The answer to that is obviously no. 

Rather, we are asking a question about the causal structure of the graph. We are invoking the $do$-operator. The $do(X=x)$ operator represents an intervention that removes the structural equation for $X$ (severing it from its causal parents) and forces $X$ to take the value $x$, creating a sub-model $M_{do(x)}$.

To say an agent "could have done otherwise" is to make a structural claim: **In the modified causal graph where we apply $do(A=a')$, the value of the moral consequence $C$ changes.** 

Formally: $C_{do(A=a')} \neq C_{do(A=a)}$.

This is Structural Sensitivity. Why does this matter? Because it differentiates agents from mere conduits. Consider an alternative graph where a man is pushed off a bridge and lands on a pedestrian. 
- $Push$: The event of being pushed.
- $Fall$: The trajectory of the man’s body.
- $C$: The pedestrian is injured.

If we intervene on the man's internal decision node—$do(\text{Decide} = \text{Try to fly})$—the consequence $C$ remains entirely unchanged. The structural equation determining $C$ depends only on gravity and mass, bypassing the man's decision node entirely. The system is structurally *insensitive* to the agent’s internal choices. Therefore, the falling man "could not have done otherwise" in a way that matters to the outcome, and he bears no moral responsibility.

However, for the agent stealing the bread, the node $A$ (the decision to steal) is structurally critical. If we apply $do(A = \text{not steal})$, the consequence $C$ is drastically altered. The agent *is* the causal bottleneck through which the future is determined. By formalizing "could have done otherwise" as $do(A=a')$, we see that determinism does not erase the causal efficacy of the agent's choices. The choice is determined, yes, but it is exactly this determined choice that structures the universe's transition from past to future.

### 6. Counterfactual Regret and the Architecture of Agency
If free will is just Structural Sensitivity, then a simple thermostat also has free will, because $do(\text{Thermostat} = \text{off})$ changes the room temperature. This is where classical compatibilism often falls short. To rescue moral agency, we must ascend to the third rung of Pearl's ladder: Counterfactuals.

A moral agent is not just a node in a causal graph. A moral agent is a computational system that *contains a representation of the causal graph* and can compute counterfactuals over it. 

Consider the evolutionary purpose of a brain capable of causal reasoning. In a deterministic but unknown universe, an organism must optimize its policy $f_A(B)$ over time. To do this, it must evaluate actions it did *not* take. After stealing the bread and being thrown in prison (Consequence $c$), the agent updates its internal model. It computes the counterfactual: 
"Given the background conditions $U=u$ that actually occurred, what would the consequence have been had I chosen not to steal?" 
Formally: $C_{A=a'}(u)$.

The agent then calculates **Counterfactual Regret** ($R$): the difference in utility between the counterfactual consequence and the actual consequence.
$R = U(C_{A=a'}(u)) - U(C_{A=a}(u))$

If $R > 0$, the agent experiences regret. This computation of regret physically alters the structural equation $f_A$ (e.g., via synaptic plasticity) so that in future, similar situations, the agent will choose differently.

**This is the very mechanism of moral agency.** Moral agency is not an exemption from the laws of physics; it is the implementation of a specific algorithm—Counterfactual Regret Minimization—within a deterministic causal graph. 

When we hold an agent morally responsible, we are asserting two things:
1. **Structural Sensitivity (Level 2):** The agent’s decision node $A$ causally determined the moral consequence $C$.
2. **Counterfactual Competence (Level 3):** The agent possesses the neuro-computational architecture to compute $C_{A=a'}(u)$, experience Counterfactual Regret, and update its behavioral policy.

A dog that bites a child possesses Structural Sensitivity (Level 2), but lacks full Counterfactual Competence (Level 3); it learns through associative conditioning (Level 1) rather than counterfactual simulation. A human with severe psychosis may have a broken causal model, rendering them incapable of accurate counterfactual computation. In both cases, our legal and moral systems intuitively reduce or eliminate culpability. We excuse them not because their actions were determined, but because their architecture lacks the structural capacity to compute counterfactual regret.

### 7. The Causal Locus of Moral Responsibility
The incompatibilist might still object: "Even if the agent computes counterfactual regret, that computation itself was necessitated by the Big Bang! The agent is still a slave to determinism."

This objection misses the structural point. The goal of assigning moral blame or praise is not to exact cosmic retribution upon an uncaused prime mover. The goal of moral practices—blaming, punishing, praising, rewarding—is to introduce new exogenous variables into the agent's causal graph to leverage their Counterfactual Competence.

When society punishes a thief, it is inserting a highly negative utility into the consequence node $C$. Because the thief is an entity that computes Counterfactual Regret, this punishment ensures that the thief's internal algorithm will evaluate future scenarios differently. 

If the universe were indeterministic—if the thief's choice $A$ was genuinely random and untethered from $B$ (their beliefs, desires, and learned policies)—then moral responsibility would be functionally useless. You cannot train a random number generator with punishment. It is precisely *because* the agent's decision-making apparatus is deterministic that moral responsibility functions at all. 

By utilizing SCMs, we can pinpoint exactly when someone is not acting freely, even in a deterministic universe. Consider a man who behaves aggressively due to a brain tumor. 
- Normal path: $Environment \rightarrow Beliefs/Desires \rightarrow Counterfactual Computation \rightarrow Action$.
- Tumor path: $Tumor \rightarrow Action$.

In the tumor scenario, the $Action$ node is bypassed by an aberrant causal edge. The standard mechanism of Counterfactual Competence is structurally disconnected from the behavior. The system is no longer sensitive to moral reasoning or counterfactual regret. The agent "could not have done otherwise" because applying a $do()$ intervention on the *Counterfactual Computation* node yields no change in the $Action$ node. This structural bypass—not determinism itself—is the true hallmark of unfreedom. 

SCMs provide the exact mathematical language to express this. We do not hold the tumor patient responsible because the causal path from external social correction to behavioral output is broken. We hold the neurotypical thief responsible because their causal path is intact. Both are fully deterministic, but structurally, they belong to entirely different classes of causal architectures.

### 8. Conclusion
The enduring deadlock between compatibilism and incompatibilism is largely a byproduct of an impoverished language for causation. By restricting ourselves to binary notions of nomological necessity (determinism) versus metaphysical openness (indeterminism), we miss the rich topological reality of the causal structures that govern our universe.

Judea Pearl’s Structural Causal Models offer a profound way out of this trap. By formalizing "could have done otherwise" as the structural sensitivity of a system to a $do()$ intervention, we rescue the Principle of Alternate Possibilities from the realm of metaphysical impossibilities. Furthermore, by identifying moral agency with the algorithmic capacity to compute Counterfactual Regret, we ground the "ghost in the machine" in solid, physical computation.

Free will is not the ability to miraculously violate the laws of physics to choose a different actual world. Free will is a property of a specific kind of causal architecture: an architecture that maps inputs to outputs through the simulation of counterfactual realities. In a deterministic universe, the capacity to imagine what "could have been" and alter our future accordingly is not an illusion. It is the very mathematical mechanism by which the universe learns, adapts, and bears the weight of moral consequence.
