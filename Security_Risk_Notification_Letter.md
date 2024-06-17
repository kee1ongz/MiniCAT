
### The Security Risk Notification Letter

To ensure that our disclosure aligns with ethical disclosure principles, we provide the letter we sent to developers as follows:

---

*Dear Developer of {Name} Mini-program,*

*We are security researchers from {Anonymization}. In our recent research on WeChat mini-programs, we extensively studied the security of the mini-programs routing mechanism. We found that under specific conditions, attackers might have the opportunity to steal or tamper with the routing parameters (i.e., information carried by `wx.navigateTo`, `wx.reLaunch`, `wx.redirectTo`). This may pose security risks to your mini-program users.*

*To illustrate, consider the following examples where you use routing to implement certain functions:*

- *Logging in with a mobile number:*  
  `wx.navigateTo({url:"/page/login?phone=190xx00"})`
- *Querying user details based on an ID:*  
  `wx.navigateTo({url:"/page/detail?id=010"})`

*Typically, this information is invisible to users. However, we discovered that by using some methods (e.g., sharing the current mini-program page in a chat), attackers can access and modify the current mini-program route. If you pass sensitive parameters or implement sensitive functions via routing, this could introduce significant security risks. For instance, with example 1, an attacker could at least obtain the user's mobile number. If there are vulnerabilities in your back-end, they might even craft a mobile number to log in as any user. In example 2, if back-end logic is not robust, attackers could potentially iterate through IDs to view unauthorized data. Based on these findings, we strongly advise carefully using the mini-programs share forwarding feature (`onShareAppMessage`) and strictly limiting forwarding unnecessary pages.*

*We have preliminarily reported these findings to Tencent. However, Tencent believes these issues are the responsibility of third-party developers. Thus, these concerns have not been officially acknowledged or rectified. But, out of responsibility for your security and that of your users, we chose to inform you of these risks via this email. If you are interested in the technical details of this issue or seek further technical support to verify these risks, please respond to this email, and we will promptly get in touch.*

*Furthermore, we wish to clarify that all our research and tests were conducted in our local environment. We did not conduct any real attacks on your mini-program or its users, and these research details have not been disclosed to the public. Security concerns every mini-program developer; we trust you will take it seriously.*

*Looking forward to your response.*
