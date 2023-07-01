import {Component} from '@angular/core';
import {HttpClient} from "@angular/common/http";

export interface Compiler {
    value: string;
    displayName: string;
}

@Component({
    selector: 'app-root',
    templateUrl: './app.component.html',
    styleUrls: ['./app.component.scss']
})
export class AppComponent {
    compilers: Compiler[] = [
        {value: 'calypsi', displayName: 'Calypsi ISO C compiler for 65816'},
    ];
    code = "int sum_numbers_1_to_x(int x) {\n" +
        "    /* Add up all numbers in sequence 1..x */\n" +
        "    int i;\n" +
        "    int sum = 0;\n" +
        "    for(i = 1; i <= x; i++) {\n" +
        "        sum += i;\n" +
        "    }\n" +
        "    return sum;\n" +
        "}"
    result = "; no result available"

    loading = false;

    constructor(private http: HttpClient) {
    }

    doCompile() {
        this.loading = true;
        this.http.post<any>("/api/compile", {code: this.code}).subscribe(result => {
            this.result = result.asm;
            this.loading = false;
        }, error => {
            this.result = "; error";
            this.loading = false;
        });
    }

    public onCodeChange(event: Event) {
        this.code = (event.target as any).value;
    }
}
