# Business Cortex Client Onboarding Questionnaire

This questionnaire helps Business Cortex understand a company from day one: who
they are, where they are going, what they want to improve, and how the agent
system should support them.

This is not meant to train a model. It is meant to give the agent enough company
context, direction, priorities, and boundaries to become useful immediately and
then improve as it learns from the business over time.

Keep answers simple. Short, honest answers are better than perfect ones.

---

## 1. Company Basics

1. What is the company name?
2. What does the company do in one or two sentences?
3. What industry are you in?
4. What locations or markets do you serve?
5. Who are your main customers?
6. What problem do you solve for customers?
7. Why do customers choose you instead of a competitor?
8. What makes the company different?
9. What should people associate with your company brand?
10. What should people never associate with your company brand?

---

## 2. Vision and Direction

11. Where do you want the company to be in 1 year?
12. Where do you want the company to be in 3 years?
13. What is the bigger vision for the company?
14. What kind of company are you trying to become?
15. What are the top 3 goals right now?
16. What is the most important goal for the next 90 days?
17. What is the biggest obstacle stopping growth?
18. What would make the next 12 months successful?
19. What would make this AI system worth keeping?
20. If the agent could help with only one thing first, what should it be?

---

## 3. Current Business Reality

21. What is working well right now?
22. What is not working well right now?
23. What tasks waste the most time?
24. What problems keep repeating?
25. Where does information usually get lost?
26. What work depends too much on one person’s memory?
27. What decisions are slow because people lack information?
28. What customer or internal issues create the most stress?
29. What tools, apps, or systems does the company currently use?
30. What system is the main source of truth for the business?

---

## 4. Customers, Sales, and Revenue

31. What does a good customer look like?
32. What does a bad-fit customer look like?
33. How do leads or customers usually come in?
34. What happens after a new lead comes in?
35. What products or services matter most to revenue?
36. What offer do you want to sell more of?
37. What are the most common customer questions?
38. What are the most common customer objections?
39. What follow-up usually needs to happen but gets missed?
40. What should the agent help with in sales or customer follow-up?

---

## 5. Operations and Team

41. Who are the key people in the company and what do they own?
42. Who makes final decisions?
43. What decisions can the agent recommend but not execute?
44. What decisions should always require human approval?
45. What daily or weekly workflows should the agent understand?
46. What reports or updates would be useful to receive automatically?
47. What should trigger an urgent alert?
48. What should be summarized instead of interrupting people immediately?
49. What does the team currently do manually that should eventually be automated?
50. What should stay human no matter what?

---

## 6. Communication Style

51. How should the company sound when speaking to customers?
52. How should the agent communicate with the owner or leadership team?
53. Should the agent be direct, careful, detailed, brief, formal, casual, or something else?
54. What words, phrases, or tone should the agent avoid?
55. What should the agent always double-check before responding?

---

## 7. Boundaries and Risk

56. What information is sensitive or private?
57. What should the agent never send, change, delete, or approve on its own?
58. What actions are safe for the agent to prepare as drafts?
59. What actions are safe only after human approval?
60. What should the agent do when it is unsure?

---

## 8. First AI Use Cases

61. What are the first 3 things you want Business Cortex to help with?
62. Which one should be built first?
63. What would the ideal result look like?
64. Who should review the agent’s work at the beginning?
65. How often should the system be reviewed or improved?

---

# After the Questionnaire

After the client answers this, Business Cortex should turn the answers into:

1. `client_profile.json` — company identity, goals, customers, tools, and users.
2. `agent_operating_rules.md` — communication style, priorities, boundaries, and escalation rules.
3. `workflow_map.md` — first workflows to automate or assist with.
4. `approval_policy.json` — what the agent can draft, recommend, approve, or never touch.
5. `first_30_days_plan.md` — the initial implementation plan.

The system should start simple, then grow with the company as more workflows,
corrections, approvals, and real business examples are captured.
