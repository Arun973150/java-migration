      * CMQGMOV - MQ Get Message Options Copybook (stub)
       01  MQGMO.
         05  MQGMO-STRUCID     PIC X(04) VALUE 'GMO '.
         05  MQGMO-VERSION     PIC S9(09) COMP VALUE 1.
         05  MQGMO-OPTIONS     PIC S9(09) COMP VALUE 0.
         05  MQGMO-WAITINTERVAL PIC S9(09) COMP VALUE 0.
