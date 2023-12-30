The following repositry consists of 3 seperate distributed system projects.

**Project 1**

  I built a very simple messaging system for health care professionals that will allow two users (such as doctors, nurses, etc.) to send and receive text messages about their work.
  It’s a client/server architecture, with a Python module that makes talking to the serve fairly easy. I designed and implemented a protocol that will make the messaging system work.
  The purpose of this project was to begin thinking about some of the issues that arise with even the most basic distributed system, especially ones that has to manage any kind of ‘state’.

**Project 2**

  In the first project,a very simple messaging system to be used by healthcare professionals using a page of PHP, hosted by a web server, to act as a central ‘state store’ was built. Building this
  far-from-optimal system highlighted several issues. In this project, I revised those issues and developed a more robust solution, by building a messaging setup using a proper message passing client and server.

**Project 3**

  For the third project, I undertook the challenge of orchestrating a wedding arrangement system.
  The goal was to arrange, as efficiently as possible, a wedding by making reservations for both a hotel to host the event and a band to play at the reception.
  This project delves into the complexities of building distributed applications that must contend with concurrency, message delays, and potential failures.

  **Problem Description**
  
    The wedding arrangement system involves making reservations for a hotel and a band, both offering slots numbered 1 to 500.
    Slot 1 represents the earliest available time, while slot 500 is the latest. The crucial requirement is that the reservation for the hotel and the band must match — if a slot i is reserved for the hotel, it must also be reserved for the band.
    Additionally, users are restricted to holding at most two reservations at any one time for both the hotel and the band.

  **Technical Implementation**
  
    In contrast to the previous two projects, this assignment adopts the HTTP protocol for content exchange and the JSON language for content description.
    The client communicates with the hotel and band services over the web, competing with other clients (classmates) to secure reservations.
    The services receive JSON messages over HTTP and support various operations, including reserving a slot, canceling a reservation, querying available slots, and checking slots reserved by the client.

  **Challenges Faced**
  
    The system introduces challenges inherent in distributed applications, such as dealing with service unavailability, non-sequential message processing, and delays in message processing.
    The services intentionally make themselves unavailable at times and introduce arbitrary delays. Notably, once the server acknowledges message receipt, it can be assumed that the message will not be lost.

  To prevent overwhelming the server, the client adheres to a rule of not sending more than one request per second.

  **Evolution from Previous Projects**
  
    This project builds upon the foundation laid in the previous two exercises. In the first project, I developed a basic messaging system for healthcare professionals, emphasizing the management of state in a distributed system.
    The second project improved upon the initial system by addressing identified issues and implementing a more robust solution using proper message passing.

  The wedding arrangement system serves as an advanced application, pushing the boundaries further by exploring the complexities of coordinating reservations in a distributed environment with additional considerations for concurrency and service reliability.
